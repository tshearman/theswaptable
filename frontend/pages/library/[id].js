import { Grid } from "@nextui-org/react";
import { LibraryCard } from "@/components/LibraryCard";

export default function Page(props) {
  return (
    <Grid.Container gap={2} justify="center" css={{ display:"flex", gap: "20px", w: "90%", margin: "auto", wrap: "wrap", "flex-direction": "row" }}>
      {props.library.map((item) => {
        return (
            <LibraryCard item={item} hidden={item.is_hidden} book_icon={false} css={{"flex-grow": 4}} key={item.id}/>
        );
      })}
    </Grid.Container>
  );
}

export const getServerSideProps = async (context) => {
  const user_id = context.params.id;
  const user_exists =
    (await fetch(`http://backend:8000/user/${user_id}`)).status == 200;

  if (!user_exists) {
    return {
      notFound: true,
    };
  }

  const items = await (
    await fetch(`http://backend:8000/library/user/${user_id}`)
  ).json();
  return { props: { user_exists: user_exists, library: items } };
};
