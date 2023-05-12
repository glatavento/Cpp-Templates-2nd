from pathlib import Path

def parse(s: str):
    for line in s.splitlines():
        if "%" not in line:
            continue
        if "section*" in line:
            is_ch = True
        elif "addcontentsline" in line:
            if "cm}" in line:
                title = line.split("cm}")[1].removesuffix("}")
            else:
                title = line.split("：")[1].removesuffix("}")
        elif "subfile" in line:
# \subfile{content/2/chapter15/0.tex}
            file = line.split("subfile{")[1].removesuffix("}").replace("content/", 'part')
            file = Path(file)
            yield is_ch, title, file
            is_ch = False

def modify_file(ch: bool, title: str, file: Path):
    ch_num = file.parent.name.replace("chapter", "ch")
    if ch:
        content = f"\section*{{{title}}}\n{file.read_text()}"
        Path(f"backmatter/Appendix/{ch_num}").mkdir(exist_ok=True)
        Path(f"backmatter/Appendix/{ch_num}.tex").write_text(content, encoding="utf-8")
        if (Path(file.parent) / "images").exists():
            Path(f"backmatter/Appendix/{ch_num}/images").mkdir(exist_ok=True)
            for img in (Path(file.parent) / "images").iterdir():
                img.rename(Path(f"backmatter/Appendix/{ch_num}/images") / img.name)
    else:
        sec_num = file.name
        content = f"\section{{{title}}}\n{file.read_text()}"
        Path(f"backmatter/Appendix/{ch_num}/{sec_num}").write_text(content, encoding="utf-8")
        with Path(f"backmatter/Appendix/{ch_num}.tex").open("a", encoding="utf-8") as f:
            f.write(f"\n\\subfile{{{ch_num}/{sec_num}}}")

if __name__ == "__main__":
    for ch, title, file in parse(Path("backmatter/Appendix.tex").read_text()):
        modify_file(ch, title, file)