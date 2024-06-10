import { Card } from "@consta/uikit/Card";
import { GridItem } from "@consta/uikit/Grid";
import { Text } from "@consta/uikit/Text";
import ReactPlayer from "react-player/lazy";
import { Badge } from "@consta/uikit/Badge";
import { Button } from "@consta/uikit/Button";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";
const Video = ({ id, preview, checksum, video, score, desc, single }) => {
  let updatedPreview = preview;
  if (preview) {
    updatedPreview = preview.replace("http://localhost:3000/", "");
  }
  let location = useLocation();
  console.log(location);

  return (
    <GridItem>
      <Card className="video-card player-wrapper ">
        {!single && (
          <Badge
            status="system"
            label={`score: ${score?.toFixed(2)}`}
            style={{ marginBottom: "10px" }}
          />
        )}
        <ReactPlayer
          url={video}
          controls={true}
          width="100%"
          min-height="100%"
          className="react-player"
        />
        <Text className="word-wrap" size="sm" style={{ marginTop: "10px" }}>
          {desc}
        </Text>
        {!single && (
          <Link to={`/video/${id}${location.search}`}>
            <Button
              label="Подробнее"
              style={{ marginTop: "20px" }}
              width="100%"
            />
          </Link>
        )}
        <Text className="word-wrap" view="ghost" size="xs">
          {checksum}
        </Text>
      </Card>
    </GridItem>
  );
};

export default Video;
