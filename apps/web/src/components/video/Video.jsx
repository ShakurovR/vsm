import { Card } from "@consta/uikit/Card";
import { GridItem } from "@consta/uikit/Grid";
import { Text } from "@consta/uikit/Text";
import ReactPlayer from "react-player/lazy";
import { Badge } from "@consta/uikit/Badge";
import { Button } from "@consta/uikit/Button";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";
import PropTypes from "prop-types";
import { reasons } from "../../data/reasons";
import { EqualHeightElement } from "react-equal-height";
const Video = ({
  id,
  checksum,
  video,
  score,
  desc,
  single,
  reason,
  audioURL,
  subtitleURL,
}) => {
  // let updatedPreview = preview;
  // if (preview) {
  //   updatedPreview = preview.replace("http://localhost:3000/", "");
  // }
  let location = useLocation();
  return (
    <GridItem style={{ width: "100%" }}>
      <Card className="video-card player-wrapper">
        <EqualHeightElement name="video">
          <div>
            <div>
              {!single && score && (
                <Badge
                  status="system"
                  label={`score: ${score?.toFixed(2)}`}
                  style={{ marginBottom: "10px", marginRight: "10px" }}
                />
              )}
              {reasons && reason && (
                <Badge
                  status="success"
                  label={`На основании: ${reasons[reason]}`}
                  style={{ marginBottom: "10px" }}
                />
              )}
            </div>

            <ReactPlayer
              url={video}
              controls={true}
              width="100%"
              min-height="100%"
              className="react-player"
            />
          </div>
          <Text className="word-wrap" size="sm" style={{ marginTop: "20px" }}>
            {desc}
          </Text>
          <div>
            {!single && (
              <Link to={`/video/${id}${location.search}`}>
                <Button
                  label="Подробнее"
                  style={{ marginTop: "20px" }}
                  width="100%"
                  className="btn_black"
                />
              </Link>
            )}
            <Text
              className="word-wrap"
              view="ghost"
              size="xs"
              style={{ marginTop: "10px" }}
            >
              {checksum}
            </Text>
          </div>
          {single && (
            <div
              style={{
                gap: "20px",
                display: "flex",
                marginTop: "20px",
                justifyContent: "center",
                paddingBottom: "50px",
              }}
            >
              {audioURL && (
                <Link
                  to={audioURL.replace(
                    "http://localhost:3000",
                    import.meta.env.VITE_HOST
                  )}
                  target="_blank"
                >
                  <Button label="Скачать аудио" className="btn_black" />
                </Link>
              )}
              {subtitleURL && (
                <Link
                  to={subtitleURL.replace(
                    "http://localhost:3000",
                    import.meta.env.VITE_HOST
                  )}
                  target="_blank"
                >
                  <Button label="Скачать субтитры" className="btn_black" />
                </Link>
              )}
            </div>
          )}
        </EqualHeightElement>
      </Card>
    </GridItem>
  );
};

export default Video;

Video.propTypes = {
  id: PropTypes.number,
  preview: PropTypes.string,
  checksum: PropTypes.string,
  video: PropTypes.string,
  score: PropTypes.number,
  desc: PropTypes.string,
  single: PropTypes.bool,
  reason: PropTypes.string,
  audioURL: PropTypes.string,
  subtitleURL: PropTypes.string,
};
