def generate_workflow(tasks):

    diagram = "graph TD\n"

    for i in range(len(tasks)-1):
        t1 = tasks[i]["task"]
        t2 = tasks[i+1]["task"]

        diagram += f"{t1} --> {t2}\n"

    return diagram