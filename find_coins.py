from collections import defaultdict
import time

denomination = [50, 25, 10, 5, 2, 1]
denomination2 = [4, 3, 1]

def find_coins_greedy(change, denomination)-> dict[str, int] | None:
    coins_by_denomination  = {}

    for coin in denomination:
        if coin > change:
            continue

        qty  = change // coin
        if qty > 0:
            coins_by_denomination[coin] = qty 
        change = change % coin

    if change > 0:
        return None
    return coins_by_denomination


def find_min_coins_up_bottom(change, denomination, memo=None) -> dict[str, int] | None:
    if memo is None: 
        memo = {}
    if change == 0:
        return {}

    if change in memo:
        return memo[change].copy()
    
    options: list[dict[int, int]] = []

    for coin in denomination:
        if coin > change:
            continue

        option = find_min_coins_up_bottom(change - coin, denomination, memo)
        if option is None:
            continue

        new_option = option.copy()
        new_option[coin] = new_option.get(coin, 0) + 1
        options.append(new_option)
    
    if not options:
        return None
    
    min_option = min(options, key=lambda option: sum(option.values()))
    memo[change] = min_option.copy()
   
    return min_option


def find_min_coins_bottom_up(change, denomination) -> dict[int, int] | None:
    if change == 0:
        return {}
    memo = {}
    memo[0] = {}

    for i in range(1, change + 1):
        for coin in denomination:
            if i - coin < 0:
                continue
           
            memo[i] = get_min(memo.get(i-coin, None), memo.get(i, None), coin)

    # print('Memo: ', memo)
    return memo.get(change)
    

def get_min(prev: dict[int, int], current: dict[int, int], coin):
    if prev is None:
        return current
    
    new_current = prev.copy()
    new_current[coin] = new_current.get(coin, 0) + 1
    if current is None:
        return new_current
    return min(new_current, current, key=lambda option: sum(option.values()))
    


def measure(func, change, denomination, label):
    start = time.perf_counter()
    result = func(change, denomination)
    elapsed = time.perf_counter() - start
    coins_count = None if result is None else sum(result.values())
    print(f"{label:12} | change={change:6} | time={elapsed:.6f}s | coins={coins_count}")


def run_tests(denomination, changes):
    print(f"\n=== denomination: {denomination} ===")
    for change in changes:
        measure(find_coins_greedy, change, denomination, "greedy")
        measure(find_min_coins_bottom_up, change, denomination, "bottom-up")
        print("-" * 55)


# тесты
run_tests(
    denomination=[50, 25, 10, 5, 2, 1],
    changes=[113, 1000, 5000, 20000]
)

run_tests(
    denomination=[4, 3, 1],
    changes=[6, 100, 1000, 5000]
)

# change = 113

# coins = find_coins_greedy(change, denomination)
# print("greedy", coins)

# coins = find_min_coins_up_bottom(change, denomination)
# print("UpBottom", coins)

# coins = find_min_coins_bottom_up(change, denomination)
# print("BottomUp", coins)


# change = 6

# coins = find_coins_greedy(change, denomination2)
# print("greedy", coins)

# coins = find_min_coins_up_bottom(change, denomination2)
# print("UpBottom", coins)

# coins = find_min_coins_bottom_up(change, denomination2)
# print("fromBottomToUp", coins)

