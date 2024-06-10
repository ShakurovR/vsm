import { Layout } from "@consta/uikit/Layout";
import { Text } from "@consta/uikit/Text";
import { Card } from "@consta/uikit/Card";
import { Grid, GridItem } from "@consta/uikit/Grid";
import "./App.css";
import SearchBlock from "./components/search/SearchBlock";
import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import React from "react";
import Video from "./components/video/Video";
const getSearch = async (value, prior) => {
  console.log("pror", prior);
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

function App() {
  const [searchValue, setSearchValue] = React.useState(null);
  const [searchPrioritet, setSearchPrioritet] = React.useState({
    video: 90,
    audio: 80,
    text: 20,
    hashtag: 30,
  });
  console.log(searchPrioritet);
  const handleSearch = (value, prioritet) => {
    console.log(prioritet);
    setSearchValue(value);
    setSearchPrioritet({ ...prioritet });
  };
  const { data, isLoading, isError } = useQuery({
    queryKey: ["search", searchValue, searchPrioritet],
    queryFn: () => getSearch(searchValue, searchPrioritet),
    enabled: !!searchValue,
    options: {
      keepPreviousData: false,
      refetchOnWindowFocus: false,
    },
  });
  console.log(data);
  return (
    <>
      <Layout direction="column">
        <Layout flex={1}>
          <Text view="primary" size="m" lineHeight="m">
            HEADER
          </Text>
        </Layout>
        <SearchBlock handleSearch={handleSearch} />
        <Layout flex={1} className="justify-center">
          <Grid
            cols={1}
            xAlign="center"
            yAlign="center"
            gap="xl"
            style={{ marginTop: "30px" }}
            breakpoints={{
              768: {
                cols: 5,
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
            {!isLoading &&
              data?.data?.map((item) => <Video key={item.id} {...item} />)}
          </Grid>
        </Layout>
      </Layout>
    </>
  );
}

export default App;
