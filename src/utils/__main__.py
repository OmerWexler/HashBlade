from utils import *

test = False
if __name__ == "__main__":
    if test:
        print('Testing non-listed analysis:')
        pc = PerformanceCalculator(16, 4600, 0.0)
        non_listed_result = pc.analyze_cpu_performance(debug=True)
        assert non_listed_result.cores == 1.0
        assert non_listed_result.frequency == 1.0
        assert non_listed_result.utilization == 1.0
        print('\nConclusion:')
        print(non_listed_result)
        print('Non-listed conclusion passed.\n\n')

        print('Testing listed analysis:')
        listed_result = pc.analyze_cpu_performance+analyze_cpu_performance_relative([4, 5, 6, 16, 9, 7, 8], [2400, 2200, 4600, 4000], debug=True)
        assert listed_result.cores == 1.0
        assert listed_result.frequency == 1.0
        assert listed_result.utilization == 1.0
        print('\nConclusion:')
        print(listed_result)
        print('Listed conclusion passed.')
    else:
        pc = PerformanceCalculator()
        non_listed_result = pc.analyze_cpu_performance(debug=True)