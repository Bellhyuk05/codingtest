"""샘플 테스트 5개로 solution.py를 확인합니다.  실행: python check.py   (이 파일은 수정하지 마세요)"""
import contextlib, importlib.util, io, os, traceback

HERE = os.path.dirname(os.path.abspath(__file__))

def _new(m):
    return m.RoomBooking()

def _eq(got, want, what):
    assert got == want, f"{what} → {got!r}, 정답 {want!r}"

# --- 샘플 테스트 5개 ---
def test_01(m):
    "정상 예약 → True"
    rb = _new(m); _eq(rb.book("A101", "월", 10, 12, "김철수"), True, "book 10~12")

def test_02(m):
    "겹치는 예약 → False"
    rb = _new(m); rb.book("A101", "월", 10, 12, "김철수")
    _eq(rb.book("A101", "월", 11, 13, "이영희"), False, "book 11~13")

def test_03(m):
    "끝나는 시각에 바로 시작 → True"
    rb = _new(m); rb.book("A101", "월", 10, 12, "김철수")
    _eq(rb.book("A101", "월", 12, 14, "이영희"), True, "book 12~14")

def test_04(m):
    "시간표 시작 순 정렬"
    rb = _new(m); rb.book("A101", "월", 14, 15, "B"); rb.book("A101", "월", 10, 12, "A")
    _eq(rb.get_schedule("A101", "월"), [(10, 12, "A"), (14, 15, "B")], "get_schedule")

def test_05(m):
    "본인 아닌 사람의 취소 → False"
    rb = _new(m); rb.book("A101", "월", 10, 12, "김철수")
    _eq(rb.cancel("A101", "월", 10, "이영희"), False, "cancel by 이영희")


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    path = os.path.join(HERE, "solution.py")
    try:
        spec = importlib.util.spec_from_file_location("solution", path)
        sol = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(sol)
    except Exception:
        print("solution.py 를 불러오지 못했습니다. 아래 에러를 Claude에게 그대로 보여 주세요.\n")
        traceback.print_exc()
        raise SystemExit(1)

    print("샘플 테스트 5개 실행\n")
    passed = 0
    for t in TESTS:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                t(sol)
            passed += 1
            print(f"  [통과] {t.__doc__}")
        except AssertionError as e:
            print(f"  [실패] {t.__doc__}  ({e})")
        except Exception as e:
            print(f"  [에러] {t.__doc__}  ({type(e).__name__}: {e})")
    print(f"\n결과: {passed} / {len(TESTS)} 통과")
    if passed == len(TESTS):
        print("5개 모두 통과! 1단계 끝. 실제 점수(80점)는 블라인드 테스트 20개로 매깁니다. 문제지 4단계 확인표까지 꼭 해 보세요.")
