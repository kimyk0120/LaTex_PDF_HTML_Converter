
import os.path as osp
import os
import subprocess
import sys
import io

print("prcs start")


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

# get only .tex, .bib file
for data in data_list:
    if data.endswith(".tex"):
        tex_file = data
    if data.endswith(".bib"):
        bib_file = data

# bib ref :  https://m31phy.tistory.com/179

# run pdflatex
subprocess_run = subprocess.run(["pdflatex", '--interaction=nonstopmode', "--output-directory=" + output_pdf_folder_path_abs,
                                 osp.join(data_folder_path_abs, tex_file)], cwd=data_folder_path_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# subprocess 0이면 정상
if subprocess_run.returncode != 0:
    print("pdflatex error")
    out_msg = subprocess_run.stdout

    buf = io.StringIO(out_msg)
    lines = buf.readlines()
    errLineNum = 0
    for cnt, line in enumerate(lines, 0):
        if line.find("!") != -1:
            errLineNum = cnt
            break

    error_lines = lines[errLineNum:errLineNum + 3]
    error_lines = [eline.strip() for eline in error_lines]
    error_message = '\n'.join(error_lines)
    print(error_message)
    # print(out_msg)
    sys.exit()

# bibtex
subprocess_run = subprocess.run(["bibtex", osp.join(output_pdf_folder_name, os.path.splitext(tex_file)[0])], cwd=data_folder_path_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# cp .bbl
subprocess_run = subprocess.run(
    ["cp", osp.join(output_pdf_folder_path_abs, os.path.splitext(tex_file)[0] + ".bbl"), data_folder_path_abs],
    cwd=data_folder_path_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)


# run pdf로
subprocess_run = subprocess.run(["pdflatex", '-interaction=nonstopmode', "--output-directory=" + output_pdf_folder_path_abs,
                                 osp.join(data_folder_path_abs, tex_file)], cwd=data_folder_path_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# run html
subprocess_run = subprocess.run(
    ["make4ht", "-d", output_html_folder_path_abs, osp.join(data_folder_path_abs, tex_file)],
    cwd=data_folder_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

# make4ht -m clean
subprocess_run = subprocess.run(["make4ht", "-m", "clean", osp.join(data_folder_path_abs, tex_file)], cwd=data_folder_path_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


print("prcs end")

def error_message():
    print("test")
