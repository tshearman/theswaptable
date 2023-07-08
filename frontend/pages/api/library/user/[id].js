export default async function users(req, res) {
  const { id } = req.query;
  const data = await fetch(`http://backend:8000/library/user/${id}`).then((r) =>
    r.json()
  );
  res.status(200).json(data);
}
