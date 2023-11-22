


bib_file_handle = open("in.bib")
html_file_handle = open("out.html", "w")
temp_write = ""
in_fields = False
manda_fields = {"author": False, "title": False, "journal": False, "year": False, "volume": False}
opt_fields = {"number": False, "pages": False, "doi": False}
bib_content = bib_file_handle.read()
lines = [a.strip() for a in bib_content.split("\n")]
checker = False
uniqkeys = []
item_infos = dict()
item_counter = bib_content.count("@")
year = ""
title = ""
author = ""
journal = ""
volume = ""
number = ""
pages = ""
doi = ""
try:
    for i in range(lines.count("")):
        lines.remove("")
    if lines[-1].strip() != "}":
        temp_write = "Input file in.bib is not a valid .bib file!"
    else:
        counter = 0                                                                #for comma checking
        for bib_line in lines:
            bib_line = bib_line.strip()
            if bib_line.strip() == "}":                                          # END OF THE ITEM
                if [i for i in manda_fields.values()] == [True] * 5:             # All mandatory fields are existent in the item
                    for fi in manda_fields.keys():
                        manda_fields[fi] = False
                    for fi in opt_fields.keys():
                        opt_fields[fi] = False
                    in_fields = False
                    counter += 1
                    item_infos[(title, author, journal, volume, number, pages, doi)] = year
                    year = ""
                    title = ""
                    author = ""
                    journal = ""
                    volume = ""
                    number = ""
                    pages = ""
                    doi = ""
                    continue
                else:                                                            # missing mandatory field(s)
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
            if not in_fields:                                                    #control @article{uniqkey
                artline = bib_line.split("{")
                if len(artline) != 2:                                              # "{" character should appear only once
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
                if artline[0].lstrip() != "@article":
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
                if (not artline[1].rstrip()[:-1].isalnum()) or artline[1].rstrip()[-1] != ",": #unique key alnum and comma check
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
                uniqkeys.append(artline[1].rstrip().rstrip(","))
                for uniqkey in uniqkeys:                                         #is unique key really unique
                    if uniqkeys.count(uniqkey) != 1:
                        checker = True
                        break
                if checker:
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
                in_fields = True
                counter += 1
            else:                                                                #IN FIELDS
                line_els = [i.strip() for i in bib_line.split("=")]             #line elements are stripped
                if line_els[0] == "title":
                    title_content = bib_line[bib_line.index("=")+1:].strip()    #title field content (not pure yet)
                if len(line_els) != 2 and line_els[0] != "title":
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
                if manda_fields.get(line_els[0]) == None and opt_fields.get(line_els[0]) == None and line_els[0] != "}":
                    temp_write = "Input file in.bib is not a valid .bib file!"                    #invalid field name
                    break
                try:
                    if not lines[counter+1].strip() == "}" and line_els[-1][-1] != ",":         #inner field comma check
                            temp_write = "Input file in.bib is not a valid .bib file!"
                            break
                    if not lines[counter + 1].strip() == "}" and not ((line_els[1][0] == line_els[-1][-2] == "\"") or (line_els[1][0]=="{" and line_els[-1][-2]=="}")): #inner field enclosing check
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                    if lines[counter + 1].strip() == "}":                                        #last field no-comma check
                        if line_els[-1][-1] == ",":
                            temp_write = "Input file in.bib is not a valid .bib file!"
                            break
                    if lines[counter + 1].strip() == "}" and not ((line_els[1][0] == line_els[-1][-1] == "\"") or (line_els[1][0] == "{" and line_els[-1][-1] == "}")): #last field enclosing check
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                except:
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
                if not lines[counter + 1] == "}":       #remove the enclosements and the comma at the end for inner field
                    line_els[-1] = line_els[-1][1:-2]
                if lines[counter + 1] == "}":           #remove the enclosements and the comma at the end for last field
                    line_els[-1] = line_els[-1][1:-1]
                if not lines[counter + 1] == "}" and line_els[0] == "title":   #remove the enclosements and the comma at the end for title (inner field)
                    try:
                        title_content = title_content[1:-2]
                    except:
                        pass
                if lines[counter + 1] == "}" and line_els[0] == "title":       #remove the enclosements and the comma at the end for title (last field)
                    try:
                        title_content = title_content[1:-1]
                    except:
                        pass
                if line_els[0] == "title" and (len(line_els) < 2 or title_content == ""):      #empty field content check for title field
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
                field_content = line_els[1]
                if field_content == "":                                           #empty field content check for the other fields
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
                if manda_fields.get(line_els[0]) == True:                         #same field is written twice
                    temp_write = "Input file in.bib is not a valid .bib file!"
                    break
                if line_els[0] == "author":
                    lfnames = field_content.split(" and ")
                    for namecheck in lfnames:               #checking if seperation by " and " is done, also made sure names does not contain ","
                        if namecheck.count(",") != 1:
                            temp_write = "Input file in.bib is not a valid .bib file!"
                            checker = True
                    if checker:
                        break
                    checknames = [i.strip().split(",") for i in lfnames]
                    for r in checknames:                                     #checking if both name and surname exists
                        if len(r) != 2 or "" in r:
                            checker = True
                            temp_write = "Input file in.bib is not a valid .bib file!"
                    if checker:
                        break
                    for ch in line_els[1]:                                   #checking if NAMES are valid
                        if not (ch.isalnum() or ch in " .,"):
                            checker = True
                            temp_write = "Input file in.bib is not a valid .bib file!"
                    if checker:
                        break
                    author = ""                                               #preparing author variable for the output
                    ctr = 1
                    for lf in lfnames:
                        fullname = ""
                        seperated = [i.strip() for i in lf.split(",")]
                        seperated.reverse()
                        fullname += seperated[0] + " " + seperated[1]
                        if ctr == len(lfnames):
                            author += fullname
                        elif ctr == len(lfnames)-1:
                            author += fullname+" and "
                        else:
                            author += fullname+", "
                        ctr += 1
                    manda_fields["author"] = True
                if line_els[0] == "title":
                    for ch in title_content:                                #checking if TITLE is valid
                        if not(ch.isalnum() or ch in ".,_-*=: "):
                            checker = True
                            temp_write = "Input file in.bib is not a valid .bib file!"
                    if checker:
                        break
                    title = title_content
                    manda_fields["title"] = True
                if line_els[0] == "journal":
                    for ch in field_content:
                        if not(ch.isalnum() or ch in ".,_ "):                #checking if JOURNAL is valid
                            checker = True
                            temp_write = "Input file in.bib is not a valid .bib file!"
                    if checker:
                        break
                    journal = field_content
                    manda_fields["journal"] = True
                if line_els[0] == "year":
                    if not(len(field_content) == 4 and field_content[0] in "12") or " " in field_content:   #checking if YEAR is valid
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                    year = field_content
                    manda_fields["year"] = True
                if line_els[0] == "volume":
                    try:                                                                    #checking if VOLUME is valid
                        if int(field_content) <= 0 or " " in field_content:
                            temp_write = "Input file in.bib is not a valid .bib file!"
                            break
                    except:
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                    volume = field_content
                    manda_fields["volume"] = True
                if line_els[0] == "number":
                    try:                                                                    #checking if NUMBER is valid
                        if int(field_content) <= 0 or " " in field_content:
                            temp_write = "Input file in.bib is not a valid .bib file!"
                            break
                    except:
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                    opt_fields["number"] = True
                    number = field_content
                if line_els[0] == "pages":
                    if field_content.count("--") != 1:                                        #checking if PAGES is valid
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                    nums = field_content.split("--")
                    if len(nums) != 2:
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                    for numb in nums:
                        try:
                            if int(numb) <= 0:
                                checker = True
                                temp_write = "Input file in.bib is not a valid .bib file!"
                        except:
                            temp_write = "Input file in.bib is not a valid .bib file!"
                            checker = True
                    if checker:
                        break
                    pages = field_content.replace("--","-")
                    opt_fields["pages"] = True
                if line_els[0] == "doi":
                    fixs = field_content.split("/")
                    if len(fixs) != 2:                                                        #checking if DOI is valid
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                    if "" in fixs:
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                    if field_content.count("/") != 1:
                        temp_write = "Input file in.bib is not a valid .bib file!"
                        break
                    for ch in field_content:
                        if not(ch.isalnum() or ch in "./"):
                            checker = True
                            temp_write = "Input file in.bib is not a valid .bib file!"
                    if checker:
                        break
                    doi = field_content
                    opt_fields["doi"] = True
                counter += 1
except:
    temp_write = "Input file in.bib is not a valid .bib file!"
if temp_write == "":
    temp_write += "<html>\n"                                          #OUTPUT WRITING
    years = [i for i in item_infos.values()]
    diffyears = []
    for yr in item_infos.values():
        if yr not in diffyears:
            diffyears.append(yr)
    diffyears.sort()
    diffyears.reverse()
    for y in diffyears:
        temp_write += f"<br> <center> <b> {y} </b> </center>\n<br>\n"
        for item in item_infos.keys():
            (t,a,j,v,n,p,d)=item
            if n != "":
                number_out=f":{n}"
            else:
                number_out=""
            if p != "":
                pages_out = f", pp. {p}"
            else:
                pages_out = ""
            if d != "":
                doi_out = f"<a href=\"https://doi.org/{d}\">link</a> "
            else:
                doi_out = ""
            if item_infos[item] == y and years.count(item_infos[item]) == 1:
                temp_write += f"[J{item_counter}] {a}, <b>{t}</b>, <i>{j}</i>, {v}{number_out}{pages_out}, {y}. {doi_out}<br>\n"
                item_counter -= 1
            if item_infos[item] == y and years.count(item_infos[item]) != 1:
                same_year_items = []
                for item in item_infos.keys():
                    if item_infos[item] == y:
                        same_year_items.append(item)
                same_year_items.sort()
                for item in same_year_items:
                    (t, a, j, v, n, p, d) = item
                    if n != "":
                        number_out = f":{n}"
                    else:
                        number_out = ""
                    if p != "":
                        pages_out = f", pp. {p}"
                    else:
                        pages_out = ""
                    if d != "":
                        doi_out = f"<a href=\"https://doi.org/{d}\">link</a> "
                    else:
                        doi_out = ""
                    temp_write += f"[J{item_counter}] {a}, <b>{t}</b>, <i>{j}</i>, {v}{number_out}{pages_out}, {y}. {doi_out}<br>\n<br>\n"
                    item_counter -= 1
                for item in same_year_items:
                    item_infos[item] = 0
                temp_write = temp_write[:-5]
    temp_write += "</html>"
html_file_handle.write(temp_write)



