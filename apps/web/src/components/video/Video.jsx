import { Card } from "@consta/uikit/Card";
import { GridItem } from "@consta/uikit/Grid";
import { Text } from "@consta/uikit/Text";
import ReactPlayer from "react-player/lazy";
import { Badge } from "@consta/uikit/Badge";
import { Button } from "@consta/uikit/Button";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";
const Video = ({ id, preview, checksum, video, score }) => {
  let updatedPreview = preview;
  if (preview) {
    updatedPreview = preview.replace("http://localhost:3000/", "");
  }
  let location = useLocation();
  console.log(location);

  return (
    <GridItem>
      <Card className="video-card player-wrapper ">
        <Badge status="system" label={`score: ${score?.toFixed(2)}`} />
        <ReactPlayer
          url={video}
          controls={true}
          width="100%"
          min-height="100%"
          className="react-player"
        />
        <Text className="word-wrap">{checksum}</Text>
        <Link to={`/video/${id}${location.search}`}>
          <Button
            label="Подробнее"
            style={{ marginTop: "20px" }}
            width="100%"
          />
        </Link>
      </Card>
    </GridItem>
  );
};

export default Video;
