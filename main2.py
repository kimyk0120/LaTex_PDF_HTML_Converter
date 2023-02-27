
import os.path as osp
import os
import subprocess
import sys
import io

print("prcs start")


def check_error(subprocess_run, print_msg=False):
    out_msg = subprocess_run.stdout
    # subprocess 0이면 정상
    if subprocess_run.returncode != 0:
        print("subprocess_run error")
        buf = io.StringIO(out_msg)
        lines = buf.readlines()
        errLineStartNum = []
        errLineEndNum = []
        errLineStartFlag = False
        errMessages = []
        for cnt, line in enumerate(lines, 0):
            if line.find("!") != -1:
                errLineStartNum.append(cnt)
                if errLineStartFlag:
                    errLineEndNum.append(cnt)
                errLineStartFlag = True
            if line.find(" ...") != -1 and errLineStartFlag:
                errLineEndNum.append(cnt)
                errLineStartFlag = False

        for errLineStart, errLineEnd in zip(errLineStartNum, errLineEndNum):
            error_lines = lines[errLineStart:errLineEnd]
            error_lines = [eline.strip() for eline in error_lines]
            error_message = '\n'.join(error_lines)
            errMessages.append(error_message)

        if len(errMessages) <= 0:
            errMessages.append(out_msg)

        print(errMessages)
        raise Exception("subprocess_run error")
    if print_msg:
        print(out_msg)


data_folder_path = "./latex_data/test1"
output_pdf_folder_name = "output_pdf"
output_html_folder_name = "output_html"

data_folder_path_abs = osp.abspath(data_folder_path)
output_pdf_folder_path_abs = osp.abspath(osp.join(data_folder_path_abs, output_pdf_folder_name))
output_html_folder_path_abs = osp.abspath(osp.join(data_folder_path_abs, output_html_folder_name))

# make output folder
if not osp.exists(data_folder_path_abs):
    os.makedirs(data_folder_path_abs)
if not osp.exists(output_pdf_folder_path_abs):
    os.makedirs(output_pdf_folder_path_abs)
if not osp.exists(output_html_folder_path_abs):
    os.makedirs(output_html_folder_path_abs)


data_list = os.listdir(data_folder_path_abs)

# get only .tex, .bib, .bblfile
tex_file = None
bib_file = None
bbl_file = None
for data in data_list:
    if data.endswith(".tex"):
        tex_file = data
    if data.endswith(".bib"):
        bib_file = data
    if data.endswith(".bbl"):
        bbl_file = data

# run latexmk pdf
subprocess_run = subprocess.run(["latexmk", '-pdf', '-shell-escape', '--interaction=nonstopmode', "--output-directory=" + output_pdf_folder_path_abs,
                                 osp.join(data_folder_path_abs, tex_file)], cwd=data_folder_path_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
check_error(subprocess_run, print_msg=True)

# latexmk clean
subprocess_run = subprocess.run(
    ["latexmk", '-c', '-shell-escape', '--interaction=nonstopmode', "--output-directory=" + output_pdf_folder_path_abs],
    cwd=data_folder_path_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
check_error(subprocess_run, print_msg=True)

# cp .bbl
if bib_file is not None and bbl_file is None:
    subprocess_run = subprocess.run(
        ["mv", osp.join(output_pdf_folder_path_abs, os.path.splitext(tex_file)[0] + ".bbl"), data_folder_path_abs],
        cwd=data_folder_path_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    check_error(subprocess_run, print_msg=True)

# run make html
subprocess_run = subprocess.run(
    ["make4ht", "--output-dir", output_html_folder_path_abs, osp.join(data_folder_path_abs, tex_file)],
    cwd=data_folder_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
check_error(subprocess_run, print_msg=True)

# make4ht clean
subprocess_run = subprocess.run(["make4ht", "-m", "clean", osp.join(data_folder_path_abs, tex_file)], cwd=data_folder_path_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
check_error(subprocess_run, print_msg=True)


print("prcs end")


if __name__ == '__main__':
    pass