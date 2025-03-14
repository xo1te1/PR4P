from flask import Flask, render_template

app = Flask(__name__)

projects = [
    {
        'id': 1,
        'name': 'Реалізація інкапсуляції та поліморфізму',
        'description': 'Реалізована інкапсуляція та поліморфізм на прикладі класичних задач обробки даних.',
        'technologies': ['Python'],
        'image': 'pr5.jpg',
        'repo_link': 'https://github.com/xo1te1/PR4P/tree/main/PR5P'
    },
    {
        'id': 2,
        'name': 'Розробка додатків із реалізацією ієрархії класів.',
        'description': 'Розроблений додаток із реалізацією ієрархії класів.',
        'technologies': ['Python'],
        'image': 'pr6.jpg',
        'repo_link': 'https://github.com/xo1te1/PR4P/tree/main/PR6P'
    }
]

@app.route('/')
def index():
    return render_template('index.html', projects=projects)

@app.route('/project/<int:project_id>')
def project(project_id):
    project = next((proj for proj in projects if proj['id'] == project_id), None)
    if project:
        return render_template('project.html', project=project)
    else:
        return "Проект не знайдено", 404

if __name__ == '__main__':
    app.run(debug=True)