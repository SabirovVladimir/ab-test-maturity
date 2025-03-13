from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Template

app = FastAPI()

# Определение категорий и их весов
category_weights = {
    "Данные и доверие к ним": 40,
    "Команда и процессы анализа": 30,
    "Процессы тестирования": 20,
    "Автоматизация тестирования": 10
}

# Полное описание категорий и уровней
score_descriptions = {
    "Данные и доверие к ним": {
        "description": "Качество данных и уровень доверия к ним в компании.",
        "subcategories": {
            "Доверие к данным": {
                "weight": 20,
                "description": "Как данные влияют на бизнес-решения.",
                "levels": {
                    0: "Данные полностью недостоверны, решения принимаются без их учёта.",
                    1: "Данные существуют, но доверие к ним минимальное, используются только в отчётах.",
                    2: "Данные влияют на решения, но остаются второстепенным фактором.",
                    3: "C-Level использует данные, но окончательные решения принимаются не только на их основе.",
                    4: "Данные — основной фактор принятия решений, их точность не вызывает сомнений."
                }
            },
            "Сбор и хранение данных": {
                "weight": 20,
                "description": "Качество инфраструктуры сбора и хранения данных.",
                "levels": {
                    0: "Данные не собираются.",
                    1: "Данные собираются хаотично, нет единой структуры.",
                    2: "Есть централизованное хранилище, но с ошибками.",
                    3: "Система данных отлажена, но возможны небольшие ошибки.",
                    4: "Данные надёжны, доступны в реальном времени, без ошибок."
                }
            }
        }
    },
    "Команда и процессы анализа": {
        "description": "Качество команды аналитиков и инженерной инфраструктуры.",
        "subcategories": {
            "Аналитики данных": {
                "weight": 15,
                "description": "Роль аналитиков в компании и их влияние на стратегию.",
                "levels": {
                    0: "Аналитиков нет.",
                    1: "Аналитики есть, но выполняют только отчётные функции.",
                    2: "Аналитики дают инсайты, но не участвуют в принятии решений.",
                    3: "Аналитики активно поддерживают A/B-тестирование.",
                    4: "Аналитики формируют продуктовую стратегию."
                }
            },
            "Инженеры данных": {
                "weight": 15,
                "description": "Качество инженерных решений в компании.",
                "levels": {
                    0: "Нет выделенной инженерной команды по данным.",
                    1: "Данные обрабатываются вручную, нет систематизированных процессов.",
                    2: "Есть базовая инфраструктура, но она нестабильна.",
                    3: "Данные надёжно хранятся, минимальные ошибки.",
                    4: "Полностью автоматизированные системы обработки данных."
                }
            }
        }
    },
    "Процессы тестирования": {
        "description": "Качество проведения A/B-тестов и их влияние на бизнес.",
        "subcategories": {
            "Частота экспериментов": {
                "weight": 10,
                "description": "Как часто и в каком масштабе проводятся A/B-тесты.",
                "levels": {
                    0: "Тесты не проводятся.",
                    1: "Запускается несколько тестов в год, нет системы.",
                    2: "Тестирование проводится, но ограничено в масштабе.",
                    3: "A/B-тестирование стало регулярным процессом.",
                    4: "Эксперименты — основа принятия решений."
                }
            }
        }
    },
    "Автоматизация тестирования": {
        "description": "Насколько автоматизирован процесс A/B-тестирования.",
        "subcategories": {
            "Автоматизация A/B-тестов": {
                "weight": 10,
                "description": "Автоматизация A/B-тестирования и интеграция в CI/CD.",
                "levels": {
                    0: "Тесты запускаются и анализируются вручную.",
                    1: "Частичная автоматизация тестов, анализ вручную.",
                    2: "Запуск тестов автоматизирован, но анализ требует ручного труда.",
                    3: "Автоматизированный процесс тестирования и анализа.",
                    4: "Полная интеграция тестов в CI/CD, автоматизированный анализ."
                }
            }
        }
    }
}


def calculate_maturity(scores):
    weighted_sum = 0
    total_weight = sum(category_weights.values())
    category_scores = {}
    recommendations = []
    next_steps = []
    
    for category, metrics in score_descriptions.items():
        category_weight = category_weights.get(category, 0)
        category_total = 0
        metric_count = len(metrics)
        
        for metric, details in metrics.items():
            metric_weight = details["weight"]
            metric_score = scores.get(metric, 0)
            category_total += metric_score * (metric_weight / 100)
        
        category_score = (category_total / metric_count) * category_weight
        category_scores[category] = category_score
        weighted_sum += category_score
    
    final_score = (weighted_sum / total_weight) * 100
    sorted_categories = sorted(category_scores.items(), key=lambda x: x[1])
    weakest_category, weakest_score = sorted_categories[0]
    
    if weakest_score <= 50:
        recommendations.append(f"Основной барьер: {weakest_category}. Нужно улучшить этот аспект перед переходом к следующему этапу.")
        if weakest_category == "Данные и доверие к ним":
            recommendations.append("📌 Внедрите систему мониторинга качества данных (Great Expectations, Monte Carlo).")
            recommendations.append("📌 Проведите аудит источников данных и настройте их верификацию.")
        elif weakest_category == "Команда и процессы анализа":
            recommendations.append("📌 Обучите аналитиков методам статистического анализа A/B-тестов.")
            recommendations.append("📌 Расширьте команду, добавив продуктового аналитика или дата-инженера.")
        elif weakest_category == "Процессы тестирования":
            recommendations.append("📌 Разработайте единые стандарты тестирования и систему документации.")
            recommendations.append("📌 Определите метрики успеха тестов и внедрите их в процессы.")
        elif weakest_category == "Автоматизация тестирования":
            recommendations.append("📌 Внедрите feature flags и автоматическое переключение на выигрышные варианты.")
            recommendations.append("📌 Используйте CI/CD для автоматизированного развертывания A/B-тестов.")
    
    if len(sorted_categories) > 1:
        next_category, next_score = sorted_categories[1]
        if next_score <= 50:
            next_steps.append(f"🚀 Следующий шаг: После улучшения {weakest_category}, займитесь {next_category}.")
    
    return final_score, category_scores, recommendations, next_steps


html_template = """<html><head>
<title>Оценка зрелости A/B-тестирования. Калькулятор Сабирова Владимира</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;700&display=swap');
body {
    background-color: #FFD700;
    color: #000000;
    font-family: 'Montserrat', sans-serif;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-y: auto;
    height: 100vh;
}
.container {
    width: 80%;
    max-width: 900px;
}
.animation-container {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 20px;
    animation: glitch 1s infinite alternate;
}
@keyframes glitch {
    0% { transform: translateX(0px); opacity: 1; text-shadow: 2px 2px #FF1493; }
    25% { transform: translateX(1px); opacity: 0.9; text-shadow: -2px -2px #00FFFF; }
    50% { transform: translateX(-1px); opacity: 0.8; text-shadow: 3px 3px #FF8C00; }
    75% { transform: translateX(2px); opacity: 0.9; text-shadow: -3px -3px #00FFEA; }
    100% { transform: translateX(0px); opacity: 1; text-shadow: 2px 2px #FF1493; }
}
details {
    margin-bottom: 10px;
}
summary {
    font-weight: bold;
    cursor: pointer;
    padding: 5px;
    background-color: transparent;
    border: none;
    font-size: 1.2em;
    text-transform: uppercase;
}
summary.subcategory {
    font-size: 1em;
    margin-left: 15px;
    color: #FF1493;
    font-weight: 600;
}
p {
    white-space: normal;
    line-height: 1.5;
    font-size: 1.1em;
    color: #222;
    font-weight: 500;
}
input[type="radio"] {
    accent-color: #FF1493;
}
button {
    background: linear-gradient(90deg, #FF1493, #FF8C00);
    border: none;
    color: #000000;
    padding: 10px 20px;
    font-size: 1.2em;
    cursor: pointer;
    text-transform: uppercase;
    font-weight: bold;
    box-shadow: 0px 0px 10px rgba(255, 20, 147, 0.8);
}
button:hover {
    filter: brightness(1.2);
}
.footer {
    position: relative;
    margin-top: 20px;
    font-size: 1em;
    color: #000000;
    font-weight: 600;
}
.footer a {
    color: #FF1493;
    text-decoration: none;
    font-weight: bold;
}
.footer a:hover {
    text-decoration: underline;
}
</style>
</head><body>
<div class="container">
    <h1>Оценка зрелости A/B-тестирования. Калькулятор Сабирова Владимира</h1>
    <form action="/" method="post">
        {% for category, metrics in score_descriptions.items() %}
            <details>
                <summary>{{ category }}</summary>
                {% for metric, desc in metrics.items() %}
                    <details>
                        <summary class="subcategory">{{ metric }}</summary>
                        <p>{{ desc["description"] | safe }}</p>
                    </details>
                    {% for score, explanation in desc["levels"].items() %}
                        <input type="radio" name="{{ metric }}" value="{{ score }}" required> {{ score }} - {{ explanation }}<br>
                    {% endfor %}
                {% endfor %}
            </details>
        {% endfor %}
        <button type="submit">Рассчитать</button>
    </form>
</div>
<div class="animation-container">
    <h1>⚡ "Write clean code," they said. ⚡<br>⚡ "Follow best practices," they said. ⚡<br>⚡ And here we are. ⚡</h1>
</div>
<div class="footer">
    Калькулятор разработан <a href="https://t.me/VladimirSabirov" target="_blank">@VladimirSabirov</a>
</div>
</body></html>"""

@app.get("/", response_class=HTMLResponse)
async def form():
    template = Template(html_template)
    return HTMLResponse(template.render(score_descriptions=score_descriptions))

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(request: Request):
    form_data = await request.form()

    # Преобразуем данные формы в числовые значения
    try:
        scores = {metric: int(value) for metric, value in form_data.items()}
    except ValueError:
        return HTMLResponse("<h1>Ошибка!</h1><p>Пожалуйста, выберите значения для всех параметров.</p>")

    final_score, category_scores, recommendations, next_steps = calculate_maturity(scores)

    result_html = """
    <h1>Ваш уровень зрелости A/B-тестирования</h1>
    <h2>Результаты по категориям:</h2>
    <ul>
    """
    for category, score in category_scores.items():
        result_html += f"<li><b>{category}</b>: {score:.2f}%</li>"
    result_html += "</ul>"
    
    result_html += f"<h2>Итоговый уровень: {final_score}%</h2>"
    
    return HTMLResponse(result_html)