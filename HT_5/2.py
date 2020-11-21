"""Програма-світлофор.
   Створити програму-емулятор світлофора для авто і пішоходів.
   Після запуска програми на екран виводиться в лівій половині - колір автомобільного, а в правій - пішохідного світлофора.
   Кожну секунду виводиться поточні кольори. Через декілька ітерацій - відбувається зміна кольорів - логіка така сама як і в звичайних світлофорах.
   Приблизний результат роботи наступний:
      Red        Green
      Red        Green
      Red        Green
      Red        Green
      Yellow     Green
      Yellow     Green
      Green      Red
      Green      Red
      Green      Red
      Green      Red
      Yellow     Red
      Yellow     Red
      Red        Green
      .......
	  """
	  
	  
import time

time_transport, time_pedestrion = list(map(int, input('Длительность светофора для транспорта и пешехода через пробел:').split()))
state_t = 'Red'
state_p = 'Green'
i=1

#время движения должно быть больше двух секунд
if time_transport <= 2 or time_pedestrion<= 2:
	print('время движения должно быть больше двух секунд')
	exit()


try:
	while True:
		print(state_t, state_p, sep='\t')
		time.sleep(1)
		time_stop = time_transport if state_p == 'Green' else time_pedestrion
		if i == time_stop:
			i = 1
			state_t = 'Green' if state_p=='Red' else 'Red'
			state_p, state_t = state_t, state_p
			
		elif time_stop - i < 3:
			state_t = 'Yellow'
			i+=1
		else:
			i+=1



except KeyboardInterrupt:
	print('Ты остановил все светофоры о_О')