from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from .models import Todo, Priority


def todo_list(request):
    """Main todo list view."""
    filter_status = request.GET.get('status', 'all')
    filter_priority = request.GET.get('priority', 'all')

    todos = Todo.objects.all()

    if filter_status == 'active':
        todos = todos.filter(completed=False)
    elif filter_status == 'completed':
        todos = todos.filter(completed=True)

    if filter_priority in ['low', 'medium', 'high']:
        todos = todos.filter(priority=filter_priority)

    total = Todo.objects.count()
    completed_count = Todo.objects.filter(completed=True).count()
    active_count = total - completed_count

    return render(request, 'todo/index.html', {
        'todos': todos,
        'priorities': Priority.choices,
        'filter_status': filter_status,
        'filter_priority': filter_priority,
        'total': total,
        'completed_count': completed_count,
        'active_count': active_count,
    })


@require_POST
def todo_create(request):
    """Create a new todo."""
    title = request.POST.get('title', '').strip()
    if not title:
        messages.error(request, 'Title is required.')
        return redirect('todo:list')

    Todo.objects.create(
        title=title,
        description=request.POST.get('description', '').strip(),
        priority=request.POST.get('priority', Priority.MEDIUM),
        due_date=request.POST.get('due_date') or None,
    )
    messages.success(request, f'Task "{title}" created successfully!')
    return redirect('todo:list')


@require_POST
def todo_toggle(request, pk):
    """Toggle todo completion status."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save(update_fields=['completed', 'updated_at'])
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'completed': todo.completed, 'id': todo.pk})
    return redirect('todo:list')


@require_POST
def todo_delete(request, pk):
    """Delete a todo."""
    todo = get_object_or_404(Todo, pk=pk)
    title = todo.title
    todo.delete()
    messages.success(request, f'Task "{title}" deleted.')
    return redirect('todo:list')


def todo_edit(request, pk):
    """Edit a todo."""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            messages.error(request, 'Title is required.')
        else:
            todo.title = title
            todo.description = request.POST.get('description', '').strip()
            todo.priority = request.POST.get('priority', Priority.MEDIUM)
            todo.due_date = request.POST.get('due_date') or None
            todo.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('todo:list')

    return render(request, 'todo/edit.html', {
        'todo': todo,
        'priorities': Priority.choices,
    })


@require_POST
def todo_clear_completed(request):
    """Delete all completed todos."""
    count, _ = Todo.objects.filter(completed=True).delete()
    messages.success(request, f'Cleared {count} completed task(s).')
    return redirect('todo:list')
