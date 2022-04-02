import random
import math

batas_x = [-5, 5]
batas_y = [-5, 5]

# Populasi


def kromosom(gen):  # Membuat kromosom dengan representasi individual menggunakan nilai integer random
    kromosomtable = []
    for i in range(gen):
        kromosomtable.append(random.randint(0, 9))
    return kromosomtable


def populasi(pop, gen):  # Menambahkan kromosom ke tiap populasi
    populasitables = []
    for i in range(pop):
        populasitables.append(kromosom(gen))
    return populasitables


def split(krom):  # Membelah kromosom menjadi 2
    return (krom[:len(krom)//2], krom[len(krom)//2:])

# Dekode kromosom


def dekode(gamet, batas):
    pengali = 0
    pembagi = 0

    # Menggunakan rumus representasi integer
    for i in range(len(gamet)):
        n = gamet[i]
        # Dengan membagi perhitungan menjadi pengali dan pembagi untuk mempermudah perhitungan
        pengali = pengali + (n*(10**-(i+1)))
        pembagi = pembagi + (9*(10**-(i+1)))
    # Menggabungkan kembali pengali dan pembagi yang sudah dihitung dan memasukkan kedalam rumus untuk menentukan fenotype
    x = batas[0] + (((batas[1]-batas[0]) / pembagi) * pengali)
    return x

# Perhitungan fitness


def fungsi(x, y):  # Menggunakan rumus fungsi dari soal
    return ((math.cos(x) + math.sin(y))**2) / (x**2 + y**2)


def fit(h):  # Nilai minimum maka digunakan 1/(h+a), a = nilai kecil agar pembagian dengan 0 tidak terjadi
    return 1//(h+0.01)


def fitness(populasi):  # Meenghitung fitness dari tiap populasi
    fitness_populasi = []
    for i in range(len(populasi)):
        x, y = split(populasi[i])
        gamet_x = dekode(x, batas_x)
        gamet_y = dekode(y, batas_y)
        f = fungsi(gamet_x, gamet_y)
        fitnes = fit(f)
        fitness_populasi.append(fitnes)
    return fitness_populasi

# Pemilihan orang tua


def select(populasi):  # Menggunakan seleksi orang tua Turnamen
    calon = []
    fitness_calon = []
    for i in range(5):  # turnamen berukuran k = 5
        # dipilih kromosom secara acak dari populasi
        n = random.randint(0, len(populasi)-1)
        calon.append(populasi[n])
    fitness_calon = fitness(calon)
    parent_1 = max(fitness_calon)
    idx_parent_1 = fitness_calon.index(parent_1)
    fitness_calon.remove(parent_1)
    parent_2 = max(fitness_calon)
    idx_parent_2 = fitness_calon.index(parent_2)
    return (calon[idx_parent_1], calon[idx_parent_2])

# Crossover(Pindah silang)


def cross(gen1, gen2, prob):  # menggunakan rekombinasi satu titik
    anak1 = []
    anak2 = []
    # menentukan titik potong secara random
    T = random.randint(1, len(gen1)-1)
    if random.random() <= prob:
        print("titik potong:", T)
        # Dibuat anak 1 dengan gen 1 - T dari gen orang tua 1
        anak1[:T] = gen1[:T]
        # Dibuat anak 1 dengan gen T+1 - G dari gen orang tua 2
        anak1[T:] = gen2[T:]
        anak2[:T] = gen2[:T]
        anak2[T:] = gen1[T:]
    else:
        anak1 = gen1
        anak2 = gen2
    return (anak1, anak2)

# Mutasi


def mutation(krom, prob):  # mutasi terjadi dengan mengganti nilai secara acak
    if random.random() <= prob:
        # posisi mutasi dipilih dengan acak
        n = random.randint(0, len(krom)-1)
        print("titik mutasi:", n)
        # nilai mutasi
        m = random.randint(0, 9)
        krom[n] = m
    return krom

# Pergantian generasi


def elitism(populasi):  # Populasi baru dipilih dengan nilai fitness terbaik dan menggantikan populasi dari generasi sebelumnya
    populasibaru = []
    fitness_populasi = fitness(populasi)
    best = max(fitness_populasi)
    idx_best = fitness_populasi.index(best)
    populasibaru.append(populasi[idx_best])
    return populasibaru


def main():
    cross_prob = 0.8
    mut_prob = 0.1
    # Inputan dari user
    print("masukan panjang gen:")
    gen = int(input())
    print("masukan banyak populasi:")
    pop = int(input())
    populasitables = populasi(pop, gen)
    print("masukan berapa generasi yang dihitung")
    generasi = int(input())
    # Memulai proses
    for i in range(generasi):
        print("\n----- generasi ke-", i+1, "-----")
        print(populasitables)
        new_tab_pop = elitism(populasitables)
        while len(new_tab_pop) < pop:
            parent_1, parent_2 = select(populasitables)
            print("parent1  parent2")
            print(parent_1, parent_2)
            anak1, anak2 = cross(parent_1, parent_2, cross_prob)
            anak1 = mutation(anak1, mut_prob)
            anak2 = mutation(anak2, mut_prob)
            print("anak1  anak2")
            print(anak1, anak2)
            new_tab_pop.append(anak1)
            if len(new_tab_pop) < pop:
                new_tab_pop.append(anak2)
        populasitables = new_tab_pop
        fitness_populasitables = fitness(populasitables)

    # cari max fitness
    maks = max(fitness_populasitables)
    # cari index max fitness
    idx_maks = fitness_populasitables.index(maks)
    print("\n----- generasi ", generasi, "-----")
    print(populasitables, "\n")
    print("maka didapatkan solusi", populasitables[idx_maks])
    print("dengan nilai fitness", fitness_populasitables[idx_maks])
    x, y = split(populasitables[idx_maks])
    fx = dekode(x, batas_x)
    fy = dekode(y, batas_y)
    print("nilai x:", fx)
    print("nilai y:", fy)
    print("nilai fungsi:", fungsi(fx, fy))


main()
