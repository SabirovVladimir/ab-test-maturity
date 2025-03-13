from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from jinja2 import Template

app = FastAPI()

# Определение показателей и их описания
score_descriptions = {
    "Data Analyst": {
        "weight": 10,
        0: "Отсутствуют аналитики.",
        1: "Аналитики есть, но занимаются только отчетами.",
        2: "Аналитики дают инсайты, но не участвуют в принятии решений.",
        3: "Аналитики поддерживают A/B тесты глубоким анализом.",
        4: "Аналитики определяют стратегию на основе данных."
    },
    "Data Engineer": {
        "weight": 10,
        0: "Нет выделенных инженеров данных.",
        1: "Инженеры есть, но нет структурированных данных.",
        2: "Есть базовые, но нестабильные конвейеры данных.",
        3: "Выстроена надежная система хранения данных.",
        4: "Продвинутая инфраструктура с автоматизацией и мониторингом."
    },
    "A/B Tests Run": {
        "weight": 8,
        0: "Тесты не запускаются.",
        1: "Запускается 1-2 теста в год.",
        2: "Запускается до 5 тестов в год.",
        3: "Запускается более 10 тестов в год.",
        4: "Тестирование - часть продуктовой культуры."
    },
    "Test Automation": {
        "weight": 8,
        0: "Полностью ручной процесс.",
        1: "Частичная автоматизация тестов.",
        2: "Автоматизирован запуск, но не анализ.",
        3: "Полная автоматизация от запуска до анализа.",
        4: "Тесты работают как часть CI/CD."
    },
    "Test Completion": {
        "weight": 6,
        0: "Большинство тестов остаются незавершенными.",
        1: "Завершается менее 25% тестов.",
        2: "Завершается 50% тестов.",
        3: "Завершается более 75% тестов.",
        4: "Практически 100% тестов завершается в срок."
    },
    "Decision Making Based on Tests": {
        "weight": 8,
        0: "Решения принимаются без тестов.",
        1: "Только 10% решений на основе тестов.",
        2: "До 30% решений основано на тестах.",
        3: "Более 50% решений принимается по результатам тестов.",
        4: "Все ключевые решения основаны на данных из тестов."
    },
    "Trust in Data": {
        "weight": 10,
        0: "Данным не доверяют.",
        1: "Данные используются, но есть сомнения.",
        2: "Данные влияют на решения, но не являются определяющими.",
        3: "C-Level использует данные, но не полагается на них полностью.",
        4: "Данные являются основой для стратегических решений."
    },
    "Data Collection and Storage": {
        "weight": 10,
        0: "Данные не собираются.",
        1: "Данные собираются эпизодически и разрознены.",
        2: "Данные документированы, но есть ошибки.",
        3: "Данные собираются комплексно, нет критических ошибок.",
        4: "Данные полностью надежны и доступны в реальном времени."
    }
}

html_template = """<html><head><title>A/B Testing Maturity</title></head><body>
<h1>A/B Testing Maturity Calculator</h1>
<form action="/" method="post">
    {% for metric, desc in score_descriptions.items() %}
        <label><b>{{ metric }}:</b></label><br>
        {% for score in range(5) %}
            <input type="radio" name="{{ metric }}" value="{{ score }}" required> {{ score }} - {{ desc[score] }}<br>
        {% endfor %}
    {% endfor %}
    <button type="submit">Calculate</button>
</form>
{% if result %}
<h2>Score: {{ result["score"] }}%</h2>
<p>Level: {{ result["level"] }}</p>
<h3>Recommendations:</h3>
<ul>
    {% for metric, value in result["details"].items() %}
        {% if value <= 1 %}
            <li><b>{{ metric }}</b>: Срочно улучшить! Это основное слабое место.</li>
        {% elif value == 2 %}
            <li><b>{{ metric }}</b>: Важно проработать в ближайшее время.</li>
        {% elif value == 3 %}
            <li><b>{{ metric }}</b>: Уже хорошо, но можно оптимизировать.</li>
        {% endif %}
    {% endfor %}
</ul>
{% endif %}
</body></html>"""

@app.get("/", response_class=HTMLResponse)
async def form():
    return Template(html_template).render(score_descriptions=score_descriptions)

@app.post("/", response_class=HTMLResponse)
async def calculate(request: Request):
    form_data = await request.form()
    scores = {key: int(form_data[key]) for key in form_data if key in score_descriptions}

    total_weight = sum(desc["weight"] for desc in score_descriptions.values())
    weighted_score = sum(scores[k] * score_descriptions[k]["weight"] for k in scores)
    
    penalty_factor = 1
    for value in scores.values():
        if value <= 1:
            penalty_factor *= 0.9
    
    final_score = ((weighted_score / total_weight) * 100) * penalty_factor
    level = "🛑 Standing Still" if final_score < 20 else "🐢 Crawling" if final_score < 40 else "🚶 Walking" if final_score < 60 else "🏃 Running" if final_score < 80 else "🚀 Flying"

    result = {"score": round(final_score, 2), "level": level, "details": scores}
    return Template(html_template).render(score_descriptions=score_descriptions, result=result)