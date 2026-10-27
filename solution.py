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


def _valid_place(room, day):
    # 리스트 같은 해시 불가능한 값이 와도 에러 없이 False가 되도록 튜플에서 비교
    return any(room == r and type(room) is str for r in ROOMS) and \
        any(day == d and type(day) is str for d in DAYS)


class RoomBooking:
    def __init__(self):
        # (room, day) -> [(start, end, name), ...]
        self._bookings = {(r, d): [] for r in ROOMS for d in DAYS}

    def book(self, room, day, start, end, name):
        if not _valid_place(room, day):
            return False
        if not (_is_int(start) and _is_int(end)):
            return False
        if start < OPEN_HOUR or end > CLOSE_HOUR:
            return False
        if start >= end:
            return False
        if end - start > MAX_HOURS:
            return False

        slots = self._bookings[(room, day)]
        for s, e, _ in slots:
            if start < e and s < end:
                return False

        count = sum(
            1
            for r in ROOMS
            for _, _, n in self._bookings[(r, day)]
            if n == name
        )
        if count >= MAX_PER_DAY:
            return False

        slots.append((start, end, name))
        return True

    def cancel(self, room, day, start, name):
        if not _valid_place(room, day) or not _is_int(start):
            return False
        slots = self._bookings[(room, day)]
        for i, (s, e, n) in enumerate(slots):
            if s == start:
                if n != name:
                    return False
                del slots[i]
                return True
        return False

    def get_schedule(self, room, day):
        if not _valid_place(room, day):
            return []
        return sorted(self._bookings[(room, day)], key=lambda b: b[0])
