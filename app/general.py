

from html import escape

#== generate HTML for the editor
def generate_form(data2lint, action):
    form = """
	<form action=\"""" + action + """\" method="POST">

	<!-- autonumber & resize example inspired by https://embed.plnkr.co/plunk/EKgvbm -->
	<div class="container">
		<div class="line-nums"><span>1</span></div>
		<textarea id="editor" name="data2lint" autofocus >""" + escape(data2lint) +"""</textarea>
	</div>
	<br/>
"""
    if action == "":
      form += """
        <input type="submit" value="Lint YAML" onclick="javascript: form.action='/lint/yaml/form';">
        <input type="submit" value="Lint JSON" onclick="javascript: form.action='/lint/json/form';"> 
"""
    else:
      form += """<input type="submit" />"""


    form += """	
        </form>
"""
    return form
