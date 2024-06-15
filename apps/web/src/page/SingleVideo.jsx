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
const getVideo = async (id, search, video, audio, text, hashtag) => {
  const data = await axios.get(`${import.meta.env.VITE_APIHOST}/video/${id}`, {
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
  const { data, isLoading, isError } = useQuery({
    queryKey: ["video", id],
    queryFn: () => getVideo(id, query, video, audio, text, hashtag),
    options: {
      keepPreviousData: true,
      refetchOnWindowFocus: true,
    },
  });

  // Use a state variable with a functional update to dynamically adjust items
  const [items, setItems] = React.useState([]);

  // Update items based on data.data.frames length after data is fetched
  React.useEffect(() => {
    if (data?.data?.frames) {
      const frameCount = data.data.frames.length;
      setItems(Array.from({ length: frameCount }, (_, i) => i));
    }
  }, [data]); // Dependency array ensures update only when data changes

  const getItemLabel = (label) => `Фрейм ${label}`;
  const [tabNumber, setTabNumber] = React.useState(0);
  console.log(tabNumber);
  if (isError) {
    return <div>Error</div>;
  }
  if (isLoading) {
    return <div>Loading</div>;
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
            id={id}
            preview={data?.data?.urls.preview}
            checksum={data?.data?.checksum}
            video={data.data.original_url}
            single={true}
            desc={data.data.description}
          />
        </GridItem>
        <GridItem>
          <Text size="3xl" align="left">
            Фреймы
          </Text>
          <Text align="left" view="secondary" style={{ marginBottom: "15px" }}>
            Мы извлекли из видео 4 вида модальностей: субтитры, звуковую
            дорожку, описание содержимого видео, пользовательское описание.
            Описание содержимого в виде мы извлекли из{" "}
            {data?.data?.frames?.length} уникальных ключевых фреймов
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
            {data.data.frames &&
              data.data.frames.map((item, index) => (
                <GridItem
                  key={index}
                  style={{ display: index === tabNumber ? "" : "none" }}
                >
                  <Arguments
                    description={item.description}
                    time={item.time}
                    id={item.id}
                    url={item.url}
                  />
                </GridItem>
              ))}
          </Grid>
        </GridItem>
      </Grid>
    </>
  );
};
export default SingleVideo;
