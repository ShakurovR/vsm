import { Grid, GridItem } from "@consta/uikit/Grid";
import { Layout } from "@consta/uikit/Layout";
import { Text } from "@consta/uikit/Text";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import React from "react";
import SearchBlock from "../components/search/SearchBlock";
import Video from "../components/video/Video";
import { useNavigate, useLocation } from "react-router-dom";
import Container from "../components/Container";
import Spech from "../components/Spech";

const getSearch = async (value, prior) => {
  const data = await axios.get(`${import.meta.env.VITE_APIHOST}/search/`, {
    params: {
      query: value,
      video: prior.video,
      audio: prior.audio,
      text: prior.text,
      hashtag: prior.hashtag,
    },
  });
  return data;
};
const Home = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const [searchValue, setSearchValue] = React.useState(
    searchParams.get("query") || null
  );
  const [searchPrioritet, setSearchPrioritet] = React.useState({
    video: parseInt(searchParams.get("video")) || 90,
    audio: parseInt(searchParams.get("audio")) || 80,
    text: parseInt(searchParams.get("text")) || 20,
    hashtag: parseInt(searchParams.get("hashtag")) || 30,
  });
  React.useEffect(() => {
    const decodedQuery = decodeURIComponent(searchParams.get("query"));
    setSearchValue(decodedQuery);
    setSearchPrioritet({
      video: parseInt(searchParams.get("video")) || 90,
      audio: parseInt(searchParams.get("audio")) || 80,
      text: parseInt(searchParams.get("text")) || 20,
      hashtag: parseInt(searchParams.get("hashtag")) || 30,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location]);
  const handleSearch = (value, prioritet) => {
    if (!value) {
      return;
    }
    const encodedValue = encodeURIComponent(value);
    setSearchValue(encodedValue);
    setSearchPrioritet({ ...prioritet });
    navigate(
      `/?query=${encodedValue}&video=${prioritet.video}&audio=${prioritet.audio}&text=${prioritet.text}&hashtag=${prioritet.hashtag}`
    );
  };

  const { data, isLoading, isError } = useQuery({
    queryKey: ["search", searchValue, searchPrioritet],
    queryFn: () => getSearch(searchValue, searchPrioritet),
    enabled:
      !!searchValue && searchValue.trim() !== "" && searchValue !== "null",
    options: {
      keepPreviousData: true,
      refetchOnWindowFocus: true,
    },
  });
  console.log(data);
  return (
    <>
      <SearchBlock handleSearch={handleSearch} />
      {data && (
        <Text
          style={{ marginTop: "20px", textAlign: "left" }}
          view="secondary"
          size="s"
        >
          В демо-режиме мы отдаем первые 10 видео с наивысшим скором.{" "}
          {`Скорость выполнения запроса в среднем 500мс`}
        </Text>
      )}
      <Layout flex={1} className="justify-center">
        {isLoading && (
          <Container>
            <Text view="primary" size="m" lineHeight="m">
              Загрузка...
            </Text>
          </Container>
        )}
        {isError && (
          <Container>
            <Text view="primary" size="m" lineHeight="m">
              Ошибка
            </Text>
          </Container>
        )}
        {data && (
          <>
            <Container>
              {data?.data?.map((item) => (
                <Video
                  key={item.id}
                  id={item.id}
                  preview={item.preview}
                  checksum={item.checksum}
                  video={item.video}
                  score={item.score}
                  single={false}
                  desc={item.description}
                  reason={item.reason}
                />
              ))}
            </Container>
          </>
        )}
        {!data && !isLoading && !isError && (
          <Grid
            cols={1}
            xAlign="center"
            yAlign="top"
            gap="xl"
            style={{ marginTop: "30px" }}
          >
            <GridItem>
              <Spech />
            </GridItem>
          </Grid>
        )}
      </Layout>
    </>
  );
};
export default Home;
