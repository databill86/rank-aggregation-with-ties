from mediane import process
from mediane.models import ResultsToProduceDecorator


def compute_result(pk):
    try:
        task = ResultsToProduceDecorator.objects.get(pk=pk)
    except:
        return
    if task.status != 1:
        return
    task.status = 2
    task.save()
    result = task.result
    task = ResultsToProduceDecorator.objects.get(pk=pk)
    if task.status != 2:
        return
    task.status = 3
    task.save()
    try:
        process.execute_median_rankings_computation_of_result(result)
        task.delete()
        result.job.update_status()
        result.job.save()
    except Exception as e:
        print(e)
        task.status = 5
        task.save()

    return