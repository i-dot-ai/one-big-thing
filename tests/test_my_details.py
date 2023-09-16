from . import utils


def test_step_through_change_details():
	client = utils.make_testino_client()
	utils.register(client, email="hi@example.com", password=None, pre_survey=True)
	page = client.get("/my-details/")
	form = page.get_form()
	form["grade"] = "HIGHER_EXECUTIVE_OFFICER"
	form["profession"] = "COMMERCIAL"
	page.has_text("Submit")
	page = form.submit().follow()
	assert page.has_text("One Big Thing overview") # homepage
	
