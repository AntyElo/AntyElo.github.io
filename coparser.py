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


def map0(s: str) -> (str, str, str):
	'shortener for room'
	if not s:
		return '', None, None
	match s:
		case ( "6-2"
			 | "Aula 6-2 Henri Coandă"
			 | "6-2 Henri Coandă" ):  return "6-2", None, None
		case ( "3-3"
			 | "3-3 Amdaris"):        return "3-3", None, None
		case "5-1":                   return "5-1", None, None
		case "Sala sportivă":         return "SSp", None, s
		case ( "D01/03"
			 | "D-01/D-03"
			 | "D01-03" ):            return "D01", "D03", None
		case ( "D02/04"
			 | "D02-04" ):            return "D02", "D04", None
		case "D-01/D-04":             return "D01", "D04", None
	if '-' in s:
		return *s.split('-', 1), None
	if '/' in s:
		return *s.split('/', 1), None
	return s, None, None


def map1(s: str) -> str:
	'shortener for subject'
	if not s:
		return '', None
	match s:
		case "Activități Individuale/În Grup":                     return s,              None
		case "Algebra Liniară Și Geometria Analitică":             return "ALGA",         s
		case "Analiza Matematică":                                 return "AM",           s
		case "Circuite Și Dispozitive Electronice":                return "CDE",          s
		case "Criptografie":                                       return "Criptografia", s
		case "Engleza În Afaceri":                                 return "EA",           s
		case "Educație Fizică":                                    return "Ed. Fizică",   s
		case "Etică Și Integritate Academică":                     return "EIA",          s
		case "Etică Și Securitatea Umană":                         return "ESU",          s
		case "Fizică":                                             return "Fizică",       s
		case "Ingineria Calculatoarelor Și Produse Program":       return "ICPP",         s
		case "Introducere În Specialitate":                        return "IS",           s
		case "Limba Română":                                       return "Română",       s
		case "Limba Engleză":                                      return "Engleză",      s
		case "Matematica Discretă":                                return "MD",           s
		case "Securitatea Și Sănătatea În Muncă":                  return "SSM",          s
		case "Proiectarea Conceptuală A Unei Aplicații Software":  return "PCAS",         s
		case "TC":                                                 return "TC",           s
		case "Tehnici De Programare":                              return "TP",           s
		case "Tehnici De Programare Aplicată":                     return "TPA",          s
		case "Programarea Calculatoarelor":                        return "PC",           s

		case "Analiza Și Proiectarea Algoritmilor":                                     return "APA",    s
		case "Analiza Și Sinteza Dispozitivelor Numerice":                              return "ASDN",   s
		case "Analiza Și Specificarea Cerințelor Software":                             return "ASCS",   s
		case "Anatomia Și Fiziologia Umană":                                            return "AFU",    s
		case "Baze De Date":                                                            return "BD",     s
		case "Bazele Statului Și Dreptului":                                            return "BSD",    s
		case "Cadrul Legal Al Securității Informaționale":                              return "CLSI",   s
		case "Circuite Electronice Integrate":                                          return "CEI",    s
		case ( "Circuite Și Dispozitive Electronice" 
			 | "1) Circuite Și Dispozitive Electronice" ):                              return "CDE",    s
		case "Dispozitive Electronice Și Mijloace Tehnice De Protecție A Informației":  return "DEMTPI", s
		case "Dispozitive Numerice Și Arhitecturi De Calculatoare":                     return "DNSAC",  s
		case "Dreptul Proprietății Intelectuale":                                       return "DPI",    s
		case "Filosofie Și Gândire Critică":                                            return "FGC",    s
		case "Filosofie Și Gândire Inginerească":                                       return "FGI",    s
		case "Fizica Corpului Solid":                                                   return "FCS",    s
		case "Integrare Europeană":                                                     return "IE",     s
		case ( "Matematici Speciale" 
			 | "2) Matematici Speciale" ):                                              return "MS",     s
		case "Măsurări Electronice":                                                    return "ME",     s
		case "Programarea Orientată Pe Obiecte":                                        return "POO",    s
		case ( "Proiectarea Asistată De Calculator A Dispozitivelor Medicale"
			 | "Proiectarea Asistată De Calculator A Dispozitivelor Medicale 1/l" ):    return "PACDM",  s
		case ( "Proiectarea Asistată În Electronică"
			 | "Proiectarea Asistată În Electronică 1/l" ):                             return "PAE",    s
		case "Structuri De Calcul Și De Comunicare":                                    return "SCC",    s
		case "Teoria Sistemelor Automate":                                              return "TSA",    s

		case _: return s, None


def map2(s: str) -> (str, str):
	'shortener for teacher'
	if not s:
		return '', None
	if s == "Gavrilița M., Cazacu C., Graur E., Malîi A., Trubca D., Capitan P.":
		return "GCGMTC", s
	return s, None

def map3(gg):
	'hints for groups'
	if len(gg) < 1:
		return ''
	return f'[{", ".join(sorted(gg))}]'

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
						buf += f'\n\t\t\t\t<td data-index="{l['slot_index']}"/>'
					elif l['subject'] == "Activități Individuale/În Grup":
						buf += f'\n\t\t\t\t<td data-index="{l['slot_index']}"><span class="palecard">{l['subject']}</span></td>'
					else:
						r, ra, rh = map0(l['room'])
						s, sh = map1(l['subject'])
						t, th = map2(l['teacher'])
						buf += f'\n\t\t\t\t<td data-index="{l['slot_index']}"><span class="card lt-{l['lesson_type']}"'
						buf +=  '' if l['slot_span'] == 1 else f' data-span="{l['slot_span']}"'
						buf += f' title="{'&#10;'.join(filter(bool, [map3(l['groups']), sh, th, rh]))}"'
						buf +=  '>'
						buf += f'\n\t\t\t\t\t<span class="room">{r}</span>'
						if ra: buf += f'\n\t\t\t\t\t<span class="roomalt">{ra}</span>'
						buf += f'\n\t\t\t\t\t<span class="subject">{s}</span>'
						buf += f'\n\t\t\t\t\t<span class="teacher">{t}</span>'
						buf +=  '\n\t\t\t\t</span></td>'
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