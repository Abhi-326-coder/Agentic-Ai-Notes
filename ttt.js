try {
    const res = await fetch('https://jsonplaceholder.typicode.com/todos/2')
    const data = await res.json(res)
    console.log(data)
} catch (error) {
    console.log(error)
}