import { Grid } from "@nextui-org/react";
import { LibraryCard } from "@/components/LibraryCard";

export default function Page(props) {
  return (
    <Grid.Container gap={2} justify="center" css={{ display:"flex", gap: "20px", w: "90%", margin: "auto", wrap: "wrap", "flex-direction": "row" }}>
      {props.library.map((item) => {
        return (
            <LibraryCard item={item} hidden={item.is_available} book_icon={true} css={{"flex-grow": 4}} key={item.id}/>
        );
      })}
    </Grid.Container>
  );
}

export const getServerSideProps = async () => {
  const items = await (
    await fetch(`http://backend:8000/items`)
  ).json();
  return { props: { library: items } };
};
