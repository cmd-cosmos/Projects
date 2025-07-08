let taskArray = [];

renderTaskList();

function renderTaskList()
{
    htmlCode = ''
    for (let i = 0; i < taskArray.length; i++){
        const task = taskArray[i];
        const {name, dueDate} = task;
        const htmlTaskAddition = `
        <div>${name}</div>
        <div>${dueDate}</div>
        <button class="deleteButton" onclick="taskArray.splice(${i},1);
        renderTaskList();
        ">Delete</button>
        `;
        htmlCode += htmlTaskAddition;
    }

    document.querySelector(".js-task-list").innerHTML = htmlCode;

}

function addTask()
{
    const inputTask = document.querySelector(".js-input");
    const inputDueDate = document.querySelector(".js-due-date");
    const taskName = inputTask.value;
    const taskDueDate = inputDueDate.value;
    taskArray.push(
        {name: taskName,
        dueDate: taskDueDate});
    inputTask.value = '';
    renderTaskList();
}





