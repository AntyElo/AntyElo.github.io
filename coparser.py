#!/usr/bin/env python3
"""parser for parser

this script parses current_scheule.json (thanks utm-curs-i-orar-2027!) and makes 
contents of tbody
"""

# class timeadd:
# 	def __init__(self, h: int, m: int):
# 		self.h = h
# 		self.m = m
# 	@classmethod
# 	def parse(cls, s: str):
# 		h, m, *_ = map(int, s.split(':'))
# 		return cls(h, m)
# 	def __add__(self, t: timeadd) -> timeadd:
# 		m1 = self.m + t.m
# 		return timeadd(self.m + t.h + (m1 // 60), m1 % 60)
# 	def __sub__(self, t: timeadd) -> timeadd:
# 		m1 = self.m - t.m
# 		return timeadd(self.m - t.h + (m1 // 60), m1 % 60)
# 	def __str__(self) -> str:
# 		return f"{self.h}:{self.m}"
# 	def __repr__(self) -> str:
# 		return f"timeadd({self.h}, {self.m})"

DAY = ['Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri']

MOCK = [[[{
	"id": None,
	"day": DAY[di],
	"slot_index": n,
	"slot_span": 1,
	"start_time": "0",
	"end_time": "0",
	"subject": None,
	"teacher": None,
	"room": None,
	"lesson_type": None,
	"subgroup": None,
	"week_parity": oe,
	"notes": [],
	"raw_text": "",
} for n in range(7)] for di in range(5)]  for oe in ("odd","even")]


def map0(s: str) -> str:
	'shortener for room'
	match s:
		case "Aula 6-2 Henri Coandă": return "6-2"
		case "6-2 Henri Coandă":      return "6-2"
		case "3-3 Amdaris":           return "3-3"
		case "Sala sportivă":         return "SSp"
		case "D01/03":                return "D01-03"
		case "D02/04":                return "D02-04"
		case _: return s


def map1(s: str) -> str:
	'shortener for subject'
	match s:
		case "Activități Individuale/În Grup":                     return "Activități Individuale/În Grup"
		case "Algebra Liniară Și Geometria Analitică":             return "ALGA"
		case "Analiza Matematică":                                 return "AM"
		case "Circuite Și Dispozitive Electronice":                return "CDE"
		case "Criptografie":                                       return "Criptografia"
		case "Engleza În Afaceri":                                 return "EA"
		case "Educație Fizică":                                    return "Ed. Fizică"
		case "Etică Și Integritate Academică":                     return "EIA"
		case "Etică Și Securitatea Umană":                         return "ESU"
		case "Fizică":                                             return "Fizică"
		case "Ingineria Calculatoarelor Și Produse Program":       return "ICPP"
		case "Introducere În Specialitate":                        return "IS"
		case "Limba Română":                                       return "L. Română"
		case "Limba Engleză":                                      return "L. Engleză"
		case "Matematica Discretă":                                return "MD"
		case "Securitatea Și Sănătatea În Muncă":                  return "SSM"
		case "Proiectarea Conceptuală A Unei Aplicații Software":  return "PCAS"
		case "TC":                                                 return "TC"
		case "Tehnici De Programare":                              return "TP"
		case "Tehnici De Programare Aplicată":                     return "TPA"
		case "Programarea Calculatoarelor":                        return "PC"
		case _: return s


def map2(s: str) -> str:
	'shortener for teacher'
	if s == "Gavrilița M., Cazacu C., Graur E., Malîi A., Trubca D., Capitan P.":
		return "GCGMTC"
	return s


def main(t):
	tt = {}

	for gg in t["groups"]:
		tt[gg["name"]] = []

	for l in t["lessons"]:
		for g in l["groups"]:
			if l['slot_span'] == 2:
				if l["week_parity"] == "both":
					l['slot_span'] = 1
					l0o = l.copy()
					l1o = l.copy()
					l0e = l.copy()
					l1e = l.copy()
					# l0['end_time']   = str(timeadd.parse(l['start_time']) + timeadd(1, 30))
					# l1['start_time'] = str(timeadd.parse(l['end_time'])   - timeadd(1, 30))
					l1o['slot_index'] += 1
					l1e['slot_index'] += 1
					l0o["week_parity"] = "odd"
					l1o["week_parity"] = "odd"
					l0e["week_parity"] = "even"
					l1e["week_parity"] = "even"
					tt[g].extend([l0o, l1o, l0e, l1e])
				else:
					l['slot_span'] = 1
					l0 = l.copy()
					l1 = l.copy()
					# l0['end_time']   = str(timeadd.parse(l['start_time']) + timeadd(1, 30))
					# l1['start_time'] = str(timeadd.parse(l['end_time'])   - timeadd(1, 30))
					l1['slot_index'] += 1
					tt[g].extend([l0, l1])
			else:
				if l["week_parity"] == "both":
					lo = l.copy()
					le = l.copy()
					lo["week_parity"] = "odd"
					le["week_parity"] = "even"
					tt[g].extend([lo, le])
				else:
					tt[g].append(l)

	for g in tt.keys():
		for di in range(5):
			td = list(filter(lambda l: l['day']==DAY[di], tt[g].copy()))
			io = list(map(lambda l: l['slot_index'], filter(lambda l: l['week_parity']!='even', td)))
			ie = list(map(lambda l: l['slot_index'], filter(lambda l: l['week_parity']!='odd',  td)))
			for n in range(min(io)):
				tt[g].append(MOCK[0][di][n])
			for n in range(min(ie)):
				tt[g].append(MOCK[1][di][n])
			for n in range(max(io)+1, 7):
				tt[g].append(MOCK[0][di][n])
			for n in range(max(ie)+1, 7):
				tt[g].append(MOCK[1][di][n])

	# DEBUG
	#with open(finpath+".co.json", "w") as fout:
	#	print(json.dumps(tt), file=fout)
	#	print(json.dumps([*set(map(lambda ll: ll.get('subject'), sum([*tt.values()], [])))]), file=fout)


	buf = ''
	for g in sorted(tt):
		buf += f'\t\t\t<tr><th tabindex="0">{g}</th>'
		for oe in ("odd", "even"):
			for d in DAY:
				buf += f"\n\t\t\t\t<!-- {d} ({oe}) -->"
				bak = {}
				for l in tt[g]:
					if l['day'] == d and l.get("week_parity") == oe:
						bak[l['slot_index']] = l
				for k in range(7):
					l = bak[k]
					if l['lesson_type'] is None:
						buf += "\n\t\t\t\t<td />"
					elif l['subject'] == "Activități Individuale/În Grup":
						buf += f'\n\t\t\t\t<td><span class="palecard">{l['subject']}</span></td>'
					else:
						buf += f'\n\t\t\t\t<td><span class="card lt-{l['lesson_type']}" data-index="{l['slot_index']}"'
						buf += '' if l['slot_span'] == 1 else f' data-span="{l['slot_span']}"'
						buf += '' if len(l['groups']) <= 1 else f' title="[{", ".join(sorted(l['groups']))}"]'
						buf += '>'
						buf += f'\n\t\t\t\t\t<span class="room">{   map0(l['room'])    if l['room']    else ''}</span>'
						buf += f'\n\t\t\t\t\t<span class="subject">{map1(l['subject']) if l['subject'] else ''}</span>'
						buf += f'\n\t\t\t\t\t<span class="teacher">{map2(l['teacher']) if l['teacher'] else ''}</span>'
						buf += '\n\t\t\t\t</span></td>'
				buf += f"\n"
		buf += f'\t\t\t</tr>\n'
	print(buf)


if __name__ == "__main__" :
	import json
	import sys

	if len(sys.argv) == 1 or "--help" in sys.argv:
		print(f"usage: {sys.argv[0]} [ --help ] {'{'} CURRENT_SCHEULE.json {'}'}", file=sys.stderr)
		exit()

	for finpath in sys.argv[1:]:
		try:
			with open(finpath, "r") as fin:
				t = json.load(fin)
		except:
			print(f"{sys.argv[0]}: '{finpath}' file is broken", file=sys.stderr)
		else:
			main(t)