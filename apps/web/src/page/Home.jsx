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
    setSearchValue(searchParams.get("query"));
    setSearchPrioritet({
      video: parseInt(searchParams.get("video")) || 90,
      audio: parseInt(searchParams.get("audio")) || 80,
      text: parseInt(searchParams.get("text")) || 20,
      hashtag: parseInt(searchParams.get("hashtag")) || 30,
    });
  }, [location]);
  const handleSearch = (value, prioritet) => {
    setSearchValue(value);
    setSearchPrioritet({ ...prioritet });
    navigate(
      `/?query=${value}&video=${prioritet.video}&audio=${prioritet.audio}&text=${prioritet.text}&hashtag=${prioritet.hashtag}`
    );
  };
  const { data, isLoading, isError } = useQuery({
    queryKey: ["search", searchValue, searchPrioritet],
    queryFn: () => getSearch(searchValue, searchPrioritet),
    enabled: !!searchValue,
    options: {
      keepPreviousData: true,
      refetchOnWindowFocus: true,
    },
  });
  console.log(data);
  return (
    <>
      <SearchBlock handleSearch={handleSearch} />
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
              />
            ))}
          </Container>
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
