import dataikuapi
import radon.raw as cc_raw
import radon.visitors as cc_visitors

    
def test_coding_recipes_complexity(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project = client.get_project(params["project"])

    recipes = project.list_recipes()
    for recipe in recipes:
        if recipe["type"] == "python":
            print(recipe)
            payload = project.get_recipe(recipe["name"]).get_settings().get_code()
            code_analysis = cc_raw.analyze(payload)
            print(code_analysis)
            assert code_analysis.loc < 100
            assert code_analysis.lloc < 50
            v = cc_visitors.ComplexityVisitor.from_code(payload)
            assert v.complexity < 21, "Code complexity of recipe " + recipe["name"] + " is too complex: " + v.complexity + " > max value (21)"
