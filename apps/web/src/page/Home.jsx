import { Grid } from "@consta/uikit/Grid";
import { Layout } from "@consta/uikit/Layout";
import { Text } from "@consta/uikit/Text";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import React from "react";
import SearchBlock from "../components/search/SearchBlock";
import Video from "../components/video/Video";
import { useNavigate } from "react-router-dom";

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
  const [searchValue, setSearchValue] = React.useState(null);
  const [searchPrioritet, setSearchPrioritet] = React.useState({
    video: 90,
    audio: 80,
    text: 20,
    hashtag: 30,
  });
  const handleSearch = (value, prioritet) => {
    console.log(prioritet);
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
        <Grid
          cols={1}
          xAlign="center"
          yAlign="top"
          gap="xl"
          style={{ marginTop: "30px" }}
          breakpoints={{
            768: {
              cols: 4,
            },
          }}
        >
          {isLoading && (
            <Text view="primary" size="m" lineHeight="m">
              Загрузка...
            </Text>
          )}
          {isError && (
            <Text view="primary" size="m" lineHeight="m">
              Ошибка
            </Text>
          )}
          {data &&
            data?.data?.map((item) => (
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
        </Grid>
      </Layout>
    </>
  );
};
export default Home;
