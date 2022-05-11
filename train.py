

learning_rate = 0.1
errors = [[], []]


def denormalized(value, list):
    return value * (max(list) - min(list)) + min(list)

def normalized(value, list):
    return (value - min(list)) / (max(list) - min(list))

def shot_procress(title):
    _fig, _ax = plt.subplots()
    _fig.set_size_inches(10, 5)
    _ax.set_title(title)
    _ax.set_xlabel('mileage')
    _ax.set_ylabel('price')
    _ax.plot(_km, line())
    _ax.scatter(_km, _price, color='green', s=50, marker='o')
    _fig.savefig("./" + title + ".png")


def save_weight(w0, w1):
    with open('weight.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["w0", "w1"])
        spamwriter.writerow([w0, w1])


def normalized_data(_km, _price):
    km = []
    price = []
    km_max = max(_km)
    price_max = max(_price)
    km_min = min(_km)
    price_min = min(_price)

    for km_i, pr_i in zip(_km, _price):
        km.append((km_i - km_min) / (km_max - km_min))
        price.append((pr_i - price_min) / (price_max - price_min))
    return km, price


def read_csv():
    _km = []
    _price = []
    with open('data.csv', 'r', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in data:
            if row[0] != 'km,price':
                splited = row[0].split(',')
                _km.append(int(splited[0]))
                _price.append(int(splited[1]))
    return _km, _price


def estimatePrice(mileage):
    global w0, w1
    predictPrice = w0 + w1 * mileage
    return predictPrice


def update_weight(epoch):
    global w0, w1

    m = 0
    error_w0 = 0
    error_w1 = 0
    for _k, _pr in zip(km, price):
        error_w0 += estimatePrice(_k) - _pr
        error_w1 += (estimatePrice(_k) - _pr) * _k
        m += 1
    w0 -= learning_rate * (error_w0 / m)
    w1 -= learning_rate * (error_w1 / m)
    collect_accuracy.append(get_accuracy(_km, _price))
    if epoch % 100 == 0:
        shot_procress("line_after_" + str(epoch) + "_epoch")
    errors[0].append(error_w0)
    errors[1].append(error_w1)


def line():
    predicted_prices = []
    for i in km:
        predicted_prices.append(denormalized(estimatePrice(i), _price))
    return predicted_prices


def get_accuracy(mileages, prices):
    price_average = sum(prices) / len(prices)
    ssr = sum(map(lambda mileage, price: pow(
        price - denormalized(estimatePrice(normalized(mileage, mileages)), prices), 2
    ), mileages, prices))
    sst = sum(map(lambda price: pow(price - price_average, 2), prices))
    return 1 - (ssr / sst)


def create_plot():
    preddicted_price = line()
    fig, (ax, ax_error, ax_accuracy) = plt.subplots(nrows=1, ncols=3)
    fig.set_size_inches(20, 5)

    ax.set_title("Result")
    ax.plot(_km, preddicted_price)
    ax.scatter(_km, _price, color='green', s=50, marker='o')
    ax.scatter(_km, preddicted_price, color='red', s=50, marker='o')
    ax.set_xlabel('mileage')
    ax.set_ylabel('price')

    ax_error.set_title("Learning proccess")
    ax_error.plot(errors[0])
    ax_error.plot(errors[1])
    ax_error.set_xlabel('epoch')
    ax_error.set_ylabel('loss')

    ax_accuracy.plot(collect_accuracy)
    ax_accuracy.set_xlabel('epoch')
    ax_accuracy.set_ylabel('accuracy')
    ax_accuracy.set_title("Accuracy")

    plt.show()


w0 = 0.0
w1 = 0.0

_km, _price = read_csv()
km, price = normalized_data(_km, _price)
collect_accuracy = []

for i in range(1000):
    update_weight(i)

# for mileage, true_price in zip(km, _price):
#     predict_price = denormalized(estimatePrice(mileage), _price)
#     print(denormalized(mileage, _km), true_price, predict_price)

save_weight(w0, w1)
create_plot()
