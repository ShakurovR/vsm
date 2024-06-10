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
      <Card>
        <Picture
          src={`${import.meta.env.VITE_HOST}/${clearUrl}`}
          className="responsive-img "
        />
        <Text>{description}</Text>
      </Card>
    </>
  );
};

export default Arguments;
