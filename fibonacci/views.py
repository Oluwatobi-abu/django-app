from django.shortcuts import render
from django.http import JsonResponse


def fibonacci_generator(n):
    """Generator function that yields Fibonacci numbers up to n terms."""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


def fibonacci_view(request):
    """Main Fibonacci page."""
    series = []
    n = None
    error = None

    if request.method == 'POST':
        try:
            n = int(request.POST.get('terms', 0))
            if n <= 0:
                error = 'Please enter a positive integer.'
            elif n > 1000:
                error = 'Please enter a number up to 1000.'
            else:
                series = list(fibonacci_generator(n))
        except (ValueError, TypeError):
            error = 'Invalid input. Please enter a valid integer.'

    return render(request, 'fibonacci/index.html', {
        'series': series,
        'n': n,
        'error': error,
    })


def fibonacci_api(request):
    """API endpoint returning Fibonacci series as JSON."""
    try:
        n = int(request.GET.get('terms', 10))
        if n <= 0 or n > 1000:
            return JsonResponse({'error': 'terms must be between 1 and 1000'}, status=400)
        series = list(fibonacci_generator(n))
        return JsonResponse({
            'terms': n,
            'series': series,
            'sum': sum(series),
            'count': len(series),
        })
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid input'}, status=400)
