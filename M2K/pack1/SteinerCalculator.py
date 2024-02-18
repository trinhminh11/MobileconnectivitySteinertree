from pack1.ToaDo import ToaDo

EPS = 10e-7
EPS2 = 10e-9
cos120 = -0.5


def trungDiem(a: ToaDo, b: ToaDo):
	x = (a.x + b.x) / 2
	y = (a.y + b.y) / 2
	return ToaDo(x, y)

def heSoA(a: ToaDo, b: ToaDo):
	if abs(a.x - b.x) < EPS2:
		return 9999

	else:
		return (a.y - b.y) / (a.x - b.x)

def heSoB(a: ToaDo, b: ToaDo):
	return a.y - heSoA(a, b) * a.x

def phiaNaoDuongThang(a, b, point: ToaDo):
	return a * point.x - point.y + b

def dinhThuBaDacViet_ver1(a: ToaDo, b: ToaDo, diemKhacPhia: ToaDo):

	trDiem = trungDiem(a, b)

	canhTamGiac = a.khoangCach(b)
	hangSo = (3**.5) * canhTamGiac / 2
	
	x1 = trDiem.x - hangSo
	x2 = trDiem.x + hangSo
	y = trDiem.y

	if diemKhacPhia.x > a.x:
		return ToaDo(x1, y)

	else:
		return ToaDo(x2, y)

def dinhThuBaDacViet_ver2(a: ToaDo, b: ToaDo, diemKhacPhia: ToaDo):

	trDiem = trungDiem(a, b)

	canhTamGiac = a.khoangCach(b)
	hangSo = (3**.5) * canhTamGiac / 2
	
	y1 = trDiem.y - hangSo
	y2 = trDiem.y + hangSo
	x = trDiem.x

	if diemKhacPhia.y > a.y:
		return ToaDo(x, y1)

	else:
		return ToaDo(x, y2)

def dinhThuBaCuaTamGiac(a: ToaDo, b: ToaDo, diemKhacPhia: ToaDo):
	trDiem = trungDiem(a, b)
	hsA = heSoA(a, b)

	if abs(hsA - 9999) < EPS2:
		return dinhThuBaDacViet_ver1(a, b, diemKhacPhia)

	if abs(hsA - 0) < EPS2:
		return dinhThuBaDacViet_ver2(a, b, diemKhacPhia)
	
	hsB = heSoB(a, b)
	hsA_TrungTruc = -1/hsA
	hsB_TrungTruc = trDiem.y - hsA_TrungTruc * trDiem.x
	canhTamGiac = a.khoangCach(b)
	hangSo = (3 ** .5) * canhTamGiac / (2 * (1 + pow(hsA_TrungTruc, 2))**.5)
	x1 = hangSo + trDiem.x
	y1 = hsA_TrungTruc * x1 + hsB_TrungTruc
	diem1 = ToaDo(x1, y1)

	x2 = -hangSo + trDiem.x
	y2 = hsA_TrungTruc * x2 + hsB_TrungTruc
	diem2 = ToaDo(x2, y2)

	if phiaNaoDuongThang(hsA, hsB, diemKhacPhia) * phiaNaoDuongThang(hsA, hsB, diem1) > 0:
		return diem2
	else:
		return diem1
	
def giaoDiemDacBiet(a: ToaDo, b: ToaDo, c: ToaDo, d: ToaDo):
	trDiem = trungDiem(a, b)
	hsA2 = heSoA(c, d)
	hsB2 = heSoB(c, d)

	return ToaDo(trDiem.x, hsA2 * trDiem.x + hsB2)

def giaoDiem(a: ToaDo, b: ToaDo, c: ToaDo, d: ToaDo):
	hsA1 = heSoA(a, b)
	hsB1 = heSoB(a, b)

	if abs(hsA1 - 9999) < EPS2:
		return giaoDiemDacBiet(a, b, c, d)
	
	hsA2 = heSoA(c, d)
	hsB2 = heSoB(c, d)

	if abs(hsA2 - 9999) < EPS2:
		return giaoDiemDacBiet(c, d, a, b)

	x = (hsB2 - hsB1) / (hsA1 - hsA2)
	y = x * hsA1 + hsB1
	return ToaDo(x, y)

def diemSteiner(d1: ToaDo, d2: ToaDo, d3: ToaDo):
	d4 = dinhThuBaCuaTamGiac(d1, d2, d3)
	d5 = dinhThuBaCuaTamGiac(d1, d3, d2)
	return giaoDiem(d4,d3,d5,d2)

def cosGocGiua(a: ToaDo, b: ToaDo, c: ToaDo):
	AB = a.khoangCach(b)
	BC = b.khoangCach(c)
	AC = a.khoangCach(c)

	return (AB*AB + BC*BC - AC*AC) / (2*AB*BC)

def lessThan120(a: ToaDo, b: ToaDo, c: ToaDo):
	cosGoc = cosGocGiua(a, b, c)

	return cosGoc > cos120 and cosGoc - cos120 > EPS
		
