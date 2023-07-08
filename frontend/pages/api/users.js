export default async function users(_, res) {
  const data = await fetch("http://backend:8000/users/").then(r => r.json())
  res.status(200).json(data)
}
