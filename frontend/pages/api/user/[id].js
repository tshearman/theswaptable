export default async function users(req, res) {
  const { user_id } = req.query;
  const data = await fetch(`http://backend:8000/user/${user_id}`).then((r) =>
    r.json()
  );
  res.status(200).json(data);
}
