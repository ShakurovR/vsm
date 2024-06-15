import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useLocation, useParams, Link, useNavigate } from "react-router-dom";
import Video from "../components/video/Video";
import { Text } from "@consta/uikit/Text";
import Arguments from "../components/arguments/Arguments";
import { Grid, GridItem } from "@consta/uikit/Grid";
import { Tabs } from "@consta/uikit/Tabs";
import React from "react";
import { Button } from "@consta/uikit/Button";
import { Badge } from "@consta/uikit/Badge";
import { reasons } from "../data/reasons";
import { Card } from "@consta/uikit/Card";

const getVideo = async (id) => {
  const data = await axios.get(`${import.meta.env.VITE_APIHOST}/video/${id}`);
  return data;
};
const getSearchData = async (id, search, video, audio, text, hashtag) => {
  const data = await axios.get(`${import.meta.env.VITE_APIHOST}/search/${id}`, {
    params: {
      query: search,
      video: video,
      audio: audio,
      text: text,
      hashtag: hashtag,
    },
  });
  return data;
};
const SingleVideo = () => {
  let location = useLocation();
  const navigate = useNavigate();
  let { id } = useParams();
  const searchParams = new URLSearchParams(location.search);
  const query = searchParams.get("query");
  const video = searchParams.get("video");
  const audio = searchParams.get("audio");
  const text = searchParams.get("text");
  const hashtag = searchParams.get("hashtag");
  const {
    data: videoData,
    isLoading: videoIsLoading,
    isError: videoIsError,
  } = useQuery({
    queryKey: ["video", id],
    queryFn: () => getVideo(id),
    options: {
      keepPreviousData: true,
      refetchOnWindowFocus: true,
    },
  });
  const { data: searchData, isLoading: searchIsLoading } = useQuery({
    queryKey: ["search", id],
    queryFn: () => getSearchData(id, query, video, audio, text, hashtag),
    options: {
      keepPreviousData: true,
      refetchOnWindowFocus: true,
    },
  });
  console.log(searchData);

  // Use a state variable with a functional update to dynamically adjust items
  const [items, setItems] = React.useState([]);

  // Update items based on data.data.frames length after data is fetched
  React.useEffect(() => {
    if (videoData?.data?.frames) {
      const frameCount = videoData.data.frames.length;
      setItems(Array.from({ length: frameCount }, (_, i) => i));
    }
  }, [videoData]); // Dependency array ensures update only when data changes

  const getItemLabel = (label) => `Фрейм ${label}`;
  const [tabNumber, setTabNumber] = React.useState(0);
  if (videoIsError) {
    return <div>Ошибка, пожалуйста попробуйте снова</div>;
  }
  if (videoIsLoading || searchIsLoading) {
    return <div>Загрузка...</div>;
  }

  return (
    <>
      <Link
        to={".."}
        onClick={(e) => {
          e.preventDefault();
          navigate(-1);
        }}
        style={{ textAlign: "right" }}
      >
        <Button
          label="К результатам поиска"
          size="xs"
          style={{ backgroundColor: "#000" }}
        />
      </Link>
      <Grid cols={2} gap="xl" xAlign="center" yAlign="top">
        <GridItem>
          <Text size="2xl" align="left">
            {query && `Запрос: ${query}`}
            {!query && `Видео`}
          </Text>
          <Text
            align="left"
            view="secondary"
            style={{ marginBottom: "15px" }}
          ></Text>
          <Video
            id={parseInt(id)}
            preview={videoData?.data?.urls.preview}
            checksum={videoData?.data?.checksum}
            video={videoData.data.original_url}
            score={searchData.data.score}
            desc={videoData.data.description}
            reason={searchData.data.reasons[0].type_data}
          />
          <div
            style={{
              gap: "20px",
              display: "flex",
              marginTop: "20px",
              justifyContent: "center",
            }}
          >
            {videoData.data.urls.audio && (
              <Link
                to={videoData.data.urls.audio.replace(
                  "http://localhost:3000",
                  import.meta.env.VITE_HOST
                )}
                target="_blank"
              >
                <Button label="Скачать аудио" className="btn_black" />
              </Link>
            )}
            {videoData.data.urls.subtitle && (
              <Link
                to={videoData.data.urls.subtitle.replace(
                  "http://localhost:3000",
                  import.meta.env.VITE_HOST
                )}
                target="_blank"
              >
                <Button label="Скачать субтитры" className="btn_black" />
              </Link>
            )}
          </div>
        </GridItem>
        <GridItem>
          <Text size="2xl" align="left">
            Фреймы
          </Text>
          <Text align="left" view="secondary" style={{ marginBottom: "15px" }}>
            Мы извлекли из видео 4 вида модальностей: субтитры, звуковую
            дорожку, описание содержимого видео, пользовательское описание.
            Описание содержимого в видео мы извлекли из{" "}
            {videoData?.data?.frames?.length} уникальных ключевых фреймов
          </Text>
          <Tabs
            value={tabNumber}
            onChange={setTabNumber}
            items={items}
            getItemLabel={getItemLabel}
            fitMode="dropdown"
          />
          <Grid
            cols={1}
            xAlign="center"
            yAlign="center"
            gap="xl"
            style={{ marginTop: "30px" }}
          >
            {videoData.data.frames &&
              videoData.data.frames.map((item, index) => (
                <GridItem
                  key={index}
                  style={{ display: index === tabNumber ? "" : "none" }}
                >
                  <Arguments description={item.description} url={item.url} />
                </GridItem>
              ))}
          </Grid>
        </GridItem>
      </Grid>
      <Grid
        cols={1}
        gap="xl"
        xAlign="center"
        yAlign="top"
        style={{ marginTop: "60px", width: "100%" }}
      >
        <GridItem style={{ width: "100%" }}>
          <Card style={{ padding: "20px", width: "100%" }}>
            <Text size="2xl" align="center">
              Причины на освании которых нейросеть сочла видео релевантным
            </Text>
            <Text style={{ marginTop: "20px" }}>
              В{" "}
              <Badge
                label={reasons[searchData.data.reasons[0].type_data]}
                size="s"
                status="normal"
              />{" "}
              был найден ключ: <Text>{searchData.data.reasons[0].content}</Text>
            </Text>
          </Card>
        </GridItem>
      </Grid>
    </>
  );
};
export default SingleVideo;
