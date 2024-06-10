import { Card } from "@consta/uikit/Card";
import { Text } from "@consta/uikit/Text";
import { Picture } from "@consta/uikit/Picture";

const Arguments = ({ description, time, id, url }) => {
  let clearUrl = url;
  if (url) {
    clearUrl = url.replace("http://localhost:3000/", "");
  }

  return (
    <>
      <Card style={{ padding: "20px" }}>
        <Text>{description}</Text>
        <Picture
          src={`${import.meta.env.VITE_HOST}/${clearUrl}`}
          className="responsive-img"
          height="300px"
        />
      </Card>
    </>
  );
};

export default Arguments;
