# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN_HOUR = 9
CLOSE_HOUR = 21
MAX_HOURS = 3
MAX_PER_DAY = 2


def _is_int(x):
    # True/False는 int의 하위 타입이지만 정수로 보지 않는다
    return type(x) is int


def _valid_room(room):
    # 리스트 같은 해시 불가능한 값이 와도 에러 없이 False가 되도록 튜플에서 비교
    return type(room) is str and room in ROOMS


def _valid_day(day):
    return type(day) is str and day in DAYS


class RoomBooking:
    def __init__(self):
        # (room, day) -> [(start, end, name), ...]
        self._bookings = {(r, d): [] for r in ROOMS for d in DAYS}
        # 마지막 book/cancel이 실패한 이유 (성공하면 빈 문자열)
        self.last_reason = ""

    def _fail(self, reason):
        self.last_reason = reason
        return False

    def book(self, room, day, start, end, name):
        if not _valid_room(room):
            return self._fail(f"없는 강의실입니다 ({', '.join(ROOMS)} 중에서 고르세요)")
        if not _valid_day(day):
            return self._fail(f"없는 요일입니다 ({', '.join(DAYS)} 중에서 고르세요)")
        if not (_is_int(start) and _is_int(end)):
            return self._fail("시각은 정수(정시)로만 예약할 수 있습니다")
        if start < OPEN_HOUR or end > CLOSE_HOUR:
            return self._fail(f"운영 시간({OPEN_HOUR:02d}:00~{CLOSE_HOUR:02d}:00)을 벗어났습니다")
        if start >= end:
            return self._fail("끝 시각이 시작 시각보다 늦어야 합니다")
        if end - start > MAX_HOURS:
            return self._fail(f"한 번에 {MAX_HOURS}시간까지만 예약할 수 있습니다")

        slots = self._bookings[(room, day)]
        for s, e, n in slots:
            if start < e and s < end:
                return self._fail(f"{s:02d}:00~{e:02d}:00 {n}님의 예약과 시간이 겹칩니다")

        count = sum(
            1
            for r in ROOMS
            for _, _, n in self._bookings[(r, day)]
            if n == name
        )
        if count >= MAX_PER_DAY:
            return self._fail(f"{name}님은 {day}요일에 이미 {MAX_PER_DAY}건을 예약했습니다 (1인 하루 {MAX_PER_DAY}건)")

        slots.append((start, end, name))
        self.last_reason = ""
        return True

    def cancel(self, room, day, start, name):
        if not _valid_room(room):
            return self._fail(f"없는 강의실입니다 ({', '.join(ROOMS)} 중에서 고르세요)")
        if not _valid_day(day):
            return self._fail(f"없는 요일입니다 ({', '.join(DAYS)} 중에서 고르세요)")
        if not _is_int(start):
            return self._fail("시작 시각은 정수(정시)로 입력하세요")
        slots = self._bookings[(room, day)]
        for i, (s, e, n) in enumerate(slots):
            if s == start:
                if n != name:
                    return self._fail(f"예약한 본인만 취소할 수 있습니다 (예약자: {n})")
                del slots[i]
                self.last_reason = ""
                return True
        return self._fail(f"{room} {day}요일 {start:02d}:00에 시작하는 예약이 없습니다")

    def get_schedule(self, room, day):
        if not (_valid_room(room) and _valid_day(day)):
            return []
        return sorted(self._bookings[(room, day)], key=lambda b: b[0])
