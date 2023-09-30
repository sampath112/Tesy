from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def sam():
    return "I LOVE YOU "


@app.route('/main', methods=['GET', 'POST'])
def upload_file():
    min_x = 0  # initial value
    max_x = 1  # initial value

    if request.method == 'POST':
        # read the uploaded file
        csv_file = request.files['csv_file']
        data = pd.read_csv(csv_file)

        X = data['bmi'].values
        Y = data['charges'].values
        max_x = np.max(X) + 100
        min_x = np.min(X) - 100

        mean_x = np.mean(X)
        mean_y = np.mean(Y)

        # total num of values
        m = len(X)

        # use formula to calculate b1 and b0
        numer = 0
        denom = 0
        for i in range(m):
            numer += (X[i] - mean_x) * (Y[i] - mean_y)
            denom += (X[i] - mean_x) ** 2
        b1 = numer / denom  # m
        b0 = mean_y - (b1 * mean_x)  # c
        ss_t = 0  # total sum of square
        ss_r = 0  # total sum of square of residuals

        for i in range(m):
            y_pred = b0 + b1 * X[i]
            ss_t += (Y[i] - mean_y) ** 2
            ss_r += (Y[i] - y_pred) ** 2
            r2 = 1 - (ss_r / ss_t)

        # calculating line values x and y
        x = np.linspace(min_x, max_x, 1000)
        y = b0 + b1 * x
        plt.plot(x, y, color='#58b970', label='regression line')

        # scatter points
        plt.scatter(X, Y, c='#ef5423', label='Scatter Points')

        plt.xlabel('BMI')
        plt.ylabel('CHARGES')
        plt.legend()

        # generate the HTML code from the plot
        from io import BytesIO
        import base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        return render_template('main.html', graphic=graphic, r2=r2, b0=b0, b1=b1)

    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=False)
