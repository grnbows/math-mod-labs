from matplotlib import pyplot as plt
import numpy as np
from numpy import std
from scipy import integrate
import random

def function():
  # return lambda x: np.log(x) / x, 0.5, 5
  # return lambda x: np.sin(x) / (1 + np.cos(x)), 2, 3
  return lambda x: x / (1 + x**2), -4, 0

def plot():
  f, a, b = function()
  x = np.linspace(a, b, 100)
  plt.plot(x, f(x))

  plt.xlabel('x')
  plt.ylabel('y')
  plt.show()

def generate_random_variables(x): 
  return [random.random() for _ in range(x)]

def get_function_max(linspaceLen):
  f, a, b = function()
  func_values = []
  for x in np.linspace(a, b, linspaceLen):
    func_values.append(f(x))
  
  return max(func_values)

class Calculator:
  @staticmethod
  def analytically():
    f, a, b = function()
    return integrate.quad(f, a, b)[0] # аналитический интеграл по Ньютона-Лейбница

  @staticmethod
  def trapezium(n):
    f, a, b = function()
    h = (b - a) / n # высота
    s = 0
    while round(a, 8) < b:
      s += 0.5 * h * (f(a) + f(a + h)) # считаем площадь
      a += h # сдвигаем левый край
    return s

class Accuracy:
  @staticmethod
  def trapezium(n):
    return Calculator.trapezium(2*n) - Calculator.trapezium(n)
    
  @staticmethod
  def one_percent(func):
    expect = np.abs(Calculator.analytically() / 100) # ожидаемый процент точности
    i = 100 # изначальный процент
    n = 1 # количество узлов 
    prev = func(n) # значение функции
    while i > expect: # итерабельно проходим пока не достигнем ожидаемой точности
      n *= 2
      trapezium = func(n)
      i = np.abs(trapezium - prev)
      prev = trapezium
    
    return n

class MonteKarlo: 
  @staticmethod
  def first(N = 100):
    f, a, b = function()
    SUM = 0
    random_values = generate_random_variables(N)
    for i in range(N):
      U =  random_values[i] * (b - a) + a
      SUM += f(U)

    return (b - a) / N * SUM
  
  @staticmethod
  def second(N):
    f, a, b = function()
    k = 0
    M = get_function_max(N)
    for _ in range(1, N + 1):
      X = a + (b - a) * random.random()
      Y = M * random.random()
      if Y < f(X):
        k += 1 

    I = M * (b - a) * k / N
    return I
    

if __name__ == '__main__':
  # plot()
  print('\n\n\n\n\n')

  first = Accuracy.one_percent(MonteKarlo.first)
  second = Accuracy.one_percent(MonteKarlo.second)

  print(f'Analytic count:         {Calculator.analytically()}')
  print(f'Trapezium method count: {Calculator.trapezium(128)}')

  print(f'Accuracy first: {first}')
  print(f'Accuracy second: {second}')

  print(f'Monte-Carlo 1st method count: {MonteKarlo.first(first)}')
  print(f'Monte-Carlo 2nd method count: {MonteKarlo.second(second)}')

  print(f'Count standard deviation for 1st method: {std([MonteKarlo.first(first)  for _ in range(100)])}')
  print(f'Count standard deviation for 2nd method: {std([MonteKarlo.second(second) for _ in range(100)])}')