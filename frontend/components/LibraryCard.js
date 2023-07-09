import { Card, Col, Row, Switch, Text, Tooltip } from "@nextui-org/react";
import { EyeOpenIcon } from "./icons/EyeOpen";
import { EyeClosedIcon } from "./icons/EyeClosed";
import { BookOpenIcon } from "./icons/BookOpen";
import { BookClosedIcon } from "./icons/BookClosed";
import styles from "../styles/LibraryCard.module.css"

export const LibraryCard = ({ item, hidden, book_icon }) => {
  return (
    <div className={styles.box}>
      { (item.is_new) ? <div className={styles.ribbon}><span>New</span></div> : null }
      <Card
        css={{
          "max-width": "300px",
          "max-height": "450px",
          "&:hover": {
            "box-shadow": "5px 10px 30px rgba(33,33,33,.5)",
          },
        }}
      >
        <Card.Body css={{ p: 0 }}>
          <Card.Image
            src={item.img_location}
            objectFit="cover"
            width="100%"
            height="100%"
            alt={item.title}
            css={{
              filter: `grayscale(${!hidden ? 1.0 : 0.0})`,
            }}
          />
        </Card.Body>
        <Card.Footer
          isBlurred
          css={{
            position: "absolute",
            bgBlur: "#00000022",
            borderTop: "$borderWeights$light solid rgba(255, 255, 255, 0.2)",
            bottom: 0,
            zIndex: 1,
            "text-shadow": "1px 1px 5px black",
          }}
        >
          <Row>
            <Col span={10}>
              <Row>
                <Col>
                  <Text color="#d1d1d1" size={14} weight="bold">
                      {item.title}
                  </Text>
                </Col>
              </Row>
            </Col>
            <Col span={2}>
              <Row>
              <Tooltip content={"Hidden items are not publicly viewable."}>
                  <Switch
                    iconOn={(book_icon) ? <BookOpenIcon /> :<EyeOpenIcon />}
                    iconOff={(book_icon) ? <BookClosedIcon /> : <EyeClosedIcon />}
                    checked={hidden}
                  />
                </Tooltip>
              </Row>
            </Col>
          </Row>
        </Card.Footer>
      </Card>
    </div>
  );
};
