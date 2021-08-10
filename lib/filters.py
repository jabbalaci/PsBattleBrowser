from common import app


@app.template_filter()
def remove_psbattle(text):
    return text.replace("PsBattle: ", "")
