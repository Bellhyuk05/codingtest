"""강의실 예약 웹페이지 — 예약 규칙은 전부 solution.py의 RoomBooking이 판단합니다."""
import os

from flask import Flask, redirect, render_template_string, request, url_for

from solution import RoomBooking

app = Flask(__name__)
rb = RoomBooking()  # 서버가 켜져 있는 동안 예약을 기억

ROOMS = ["A101", "A102", "B201"]
DAYS = ["월", "화", "수", "목", "금"]


def to_number(text):
    # 화면 입력값을 숫자로 바꿔 그대로 넘길 뿐, 맞는지 틀린지는 solution.py가 정한다
    text = (text or "").strip()
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    return text


PAGE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>강의실 예약</title>
<style>
  :root { --bg:#f5f6f8; --card:#fff; --text:#1d2129; --muted:#6b7280; --line:#e3e6ea;
          --accent:#2f6fed; --ok:#15803d; --okbg:#dcfce7; --fail:#b91c1c; --failbg:#fee2e2; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--text);
         font-family:system-ui,-apple-system,"Malgun Gothic","Apple SD Gothic Neo",sans-serif; }
  main { max-width:720px; margin:0 auto; padding:24px 16px 48px; }
  h1 { font-size:24px; margin:0 0 4px; }
  .sub { color:var(--muted); margin:0 0 20px; font-size:14px; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:12px;
          padding:18px; margin-bottom:16px; }
  h2 { font-size:17px; margin:0 0 12px; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(110px,1fr)); gap:10px; }
  label { display:flex; flex-direction:column; font-size:13px; color:var(--muted); gap:4px; }
  input, select { font:inherit; font-size:16px; padding:9px 10px; border:1px solid var(--line);
                  border-radius:8px; background:#fff; color:var(--text); width:100%; }
  button { font:inherit; font-size:16px; font-weight:600; margin-top:12px; padding:10px 18px;
           border:0; border-radius:8px; background:var(--accent); color:#fff; cursor:pointer; }
  button.secondary { background:#4b5563; }
  .result { border-radius:12px; padding:18px; margin-bottom:16px; font-size:28px; font-weight:800;
            text-align:center; }
  .result small { display:block; font-size:14px; font-weight:500; margin-top:6px; }
  .ok { background:var(--okbg); color:var(--ok); border:2px solid var(--ok); }
  .fail { background:var(--failbg); color:var(--fail); border:2px solid var(--fail); }
  table { width:100%; border-collapse:collapse; margin-top:12px; font-size:15px; }
  th, td { text-align:left; padding:8px; border-bottom:1px solid var(--line); }
  .empty { color:var(--muted); margin-top:12px; }
</style>
</head>
<body>
<main>
  <h1>강의실 예약</h1>
  <p class="sub">운영 시간 9시~21시 · 1회 최대 3시간 · 1인 하루 2건</p>

  {% if result is not none %}
  <div class="result {{ 'ok' if result else 'fail' }}" id="result">
    {{ '성공' if result else '실패' }}
    <small>{{ message }}</small>
  </div>
  {% endif %}

  <section class="card">
    <h2>예약하기</h2>
    <form method="post" action="{{ url_for('book') }}">
      <div class="grid">
        <label>강의실<select name="room">{% for r in rooms %}<option {{ 'selected' if r == f.room }}>{{ r }}</option>{% endfor %}</select></label>
        <label>요일<input name="day" value="{{ f.day }}" list="days" required></label>
        <label>시작(시)<input name="start" value="{{ f.start }}" inputmode="decimal" required></label>
        <label>끝(시)<input name="end" value="{{ f.end }}" inputmode="decimal" required></label>
        <label>이름<input name="name" value="{{ f.name }}" required></label>
      </div>
      <button type="submit">예약</button>
    </form>
  </section>

  <section class="card">
    <h2>취소하기</h2>
    <form method="post" action="{{ url_for('cancel') }}">
      <div class="grid">
        <label>강의실<select name="room">{% for r in rooms %}<option {{ 'selected' if r == f.room }}>{{ r }}</option>{% endfor %}</select></label>
        <label>요일<input name="day" value="{{ f.day }}" list="days" required></label>
        <label>시작(시)<input name="start" value="{{ f.start }}" inputmode="decimal" required></label>
        <label>이름<input name="name" value="{{ f.name }}" required></label>
      </div>
      <button type="submit" class="secondary">취소</button>
    </form>
  </section>

  <section class="card">
    <h2>시간표 보기</h2>
    <form method="get" action="{{ url_for('index') }}">
      <div class="grid">
        <label>강의실<select name="room">{% for r in rooms %}<option {{ 'selected' if r == view_room }}>{{ r }}</option>{% endfor %}</select></label>
        <label>요일<select name="day">{% for d in days %}<option {{ 'selected' if d == view_day }}>{{ d }}</option>{% endfor %}</select></label>
      </div>
      <button type="submit" class="secondary">보기</button>
    </form>
    <h2 style="margin-top:16px">{{ view_room }} · {{ view_day }}요일</h2>
    {% if schedule %}
    <table>
      <tr><th>시간</th><th>예약자</th></tr>
      {% for s, e, n in schedule %}<tr><td>{{ s }}~{{ e }}시</td><td>{{ n }}</td></tr>{% endfor %}
    </table>
    {% else %}
    <p class="empty">예약이 없습니다.</p>
    {% endif %}
  </section>

  <datalist id="days">{% for d in days %}<option value="{{ d }}">{% endfor %}</datalist>
</main>
</body>
</html>"""


def render(result=None, message="", form=None, view_room=None, view_day=None):
    form = form or {}
    view_room = view_room or form.get("room") or ROOMS[0]
    view_day = view_day or form.get("day") or DAYS[0]
    return render_template_string(
        PAGE,
        result=result,
        message=message,
        f={k: form.get(k, "") for k in ("room", "day", "start", "end", "name")},
        rooms=ROOMS,
        days=DAYS,
        view_room=view_room,
        view_day=view_day,
        schedule=rb.get_schedule(view_room, view_day),
    )


@app.get("/")
def index():
    return render(view_room=request.args.get("room"), view_day=request.args.get("day"))


@app.post("/book")
def book():
    f = request.form
    ok = rb.book(f.get("room"), f.get("day", "").strip(), to_number(f.get("start")),
                 to_number(f.get("end")), f.get("name", "").strip())
    msg = f"{f.get('name')} · {f.get('room')} · {f.get('day')} · {f.get('start')}~{f.get('end')}시 예약"
    return render(ok, msg + (" 완료" if ok else "이 거절되었습니다"), f)


@app.post("/cancel")
def cancel():
    f = request.form
    ok = rb.cancel(f.get("room"), f.get("day", "").strip(), to_number(f.get("start")),
                   f.get("name", "").strip())
    msg = f"{f.get('name')} · {f.get('room')} · {f.get('day')} · {f.get('start')}시 예약 취소"
    return render(ok, msg + (" 완료" if ok else "가 거절되었습니다"), f)


@app.get("/book")
@app.get("/cancel")
def back_home():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
