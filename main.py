def check_if_terminal(node):
	return node in end_states

def invalid_move(cell, move):
	x = cell[0] + move[0]
	y = cell[1] + move[1]
	if(x < 0 or x >= N or y < 0 or y >= M):
		return True
	node = (x, y)
	if node in wall_states:
		return True
	return False

def reward(cell, move):
	if(move == (-1, -1)):
		#it is an end node
		return rewards[cell[0]][cell[1]]

	return rewards[cell[0]][cell[1]] + unit_step_cost
	# Can be modified according to the defn of R(I, A)

def alternate_map(move):
	if(move[1] == 0):
		return [(0,1), (0, -1)]
	return [(1,0), (-1, 0)]

def possibility_sum(cell, move):
	sum = 0
	p = 0.8
	if(invalid_move(cell, move)):
		sum += p * utility[cell[0]][cell[1]]
	else:
		sum += p * utility[cell[0] + move[0]][cell[1] + move[1]]

	p = 0.1

	moves = alternate_map(move)

	for move in moves:
		if(invalid_move(cell, move)):
			sum += p * utility[cell[0]][cell[1]]
		else:
			sum += p * utility[cell[0] + move[0]][cell[1] + move[1]]

	return sum

def move_map(move):
	if(move == (1,0)):
		return 'B'
	elif(move == (-1, 0)):
		return 'T'
	elif(move == (0, 1)):
		return 'R'
	return 'L'

buffer = input().split()

N = int(buffer[0])
M = int(buffer[1])
# N rows, M columns
# N = 2, M = 4:
# _ _ _ _
# _ _ _ _


rewards = []
for i in range(0, N):
	rewards.append([])

for i in range(0, N):
	buffer = input().split()
	for j in range(0, M):
		store = float(buffer[j])
		rewards[i].append(store)

# rewards matrix filled

buffer = input().split()
count_end_states = int(buffer[0])
count_wall_states = int(buffer[1])

end_states = []
for i in range(0, count_end_states):
	buffer = input().split()
	x = int(buffer[0])
	y = int(buffer[1])
	end_states.append((x, y))

wall_states = []
for i in range(0, count_wall_states):
	buffer = input().split()
	x = int(buffer[0])
	y = int(buffer[1])
	wall_states.append((x, y))

buffer = input().split()
x = int(buffer[0])
y = int(buffer[1])

start_state = (x, y)

unit_step_cost = float(input())
# inputs taken

# utility matrix being created
utility = []
for i in range(0, N):
	utility.append([])

for i in range(0, N):
	for j in range(0, M):
		utility[i].append(rewards[i][j])

action_list = [(0, 1), (0, -1), (-1, 0), (1, 0) ]

discount = 0.99

iter_count = 0

while(1):
	print("Iteration: ", iter_count, "\n")
	iter_count += 1
	break_flag = 1

	new_utility = []
	for i in range(0, N):
		new_utility.append([])

	for i in range(0, N):
		for j in range(0, M):
			new_utility[i].append(0)
	# creating a new utility array to write the utilities to

	for i in range(0, N):
		for j in range(0, M):
			# for each cell of the utility array

			move_number = 0
			present_max = 0

			if(check_if_terminal((i, j))):
				present_max = reward((i, j), (-1, -1))
				# with (-1, -1): get the reward in the terminal state

			else:
				for move in action_list:
					# maximize over the actions

					reward_accrued = reward((i, j), move)
					# the R(state, action) factor
					summation = possibility_sum((i, j), move)
					# the summation over next states factor
					if(move_number == 0):
						present_max = reward_accrued + discount * summation

					else:
						present_max = max(present_max, reward_accrued + discount * summation)
					move_number += 1

			new_utility[i][j] = present_max

			util_change = abs(new_utility[i][j] - utility[i][j])
			if(util_change > 0.01 * abs(utility[i][j])):
				break_flag = 0

	for i in range(0, N):
		for j in range(0, M):
			print(round(new_utility[i][j], 3), end = "\t")
			utility[i][j] = new_utility[i][j]
		print("\n")

	if(break_flag == 1):
		break

policy = []
for i in range(0, N):
	policy.append([])

for i in range(0, N):
	for j in range(0, M):
		policy[i].append(0)

# Finding the Policy
print("Policy:")
for i in range(0, N):
	for j in range(0, M):
		# for each cell of the policy array

		move_number = 0
		present_max = 0
		best_move = (-1, -1)

		if((i, j) in wall_states or (i, j) in end_states):
			policy[i][j] = '-'

		else:
			for move in action_list:
				# maximize over the actions
				reward_accrued = 0
				# the R(state, action) factor
				summation = possibility_sum((i, j), move)
				# the summation over next states factor
				if(move_number == 0):
					present_max = reward_accrued + summation
					best_move = move

				else:
					present_max = max(present_max, reward_accrued + summation)
					if(present_max == reward_accrued + summation):
						best_move = move

				move_number += 1

			policy[i][j] = move_map(best_move)

		print(policy[i][j]," ",round(present_max,3), end = " ")
	print()
