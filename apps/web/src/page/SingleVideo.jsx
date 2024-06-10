import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useLocation } from "react-router-dom";
import { useParams } from "react-router-dom";
import Video from "../components/video/Video";
import { Text } from "@consta/uikit/Text";
import Arguments from "../components/arguments/Arguments";
import { Grid, GridItem } from "@consta/uikit/Grid";

const getVideo = async (id) => {
  const data = await axios.get(`${import.meta.env.VITE_APIHOST}/video/${id}`);
  return data;
};
const SingleVideo = () => {
  let location = useLocation();
  let { id } = useParams();

  const { data, isLoading, isError } = useQuery({
    queryKey: ["video", id],
    queryFn: () => getVideo(id),
    options: {
      keepPreviousData: true,
      refetchOnWindowFocus: true,
    },
  });

  console.log(data);
  if (isError) {
    return <div>Error</div>;
  }
  if (isLoading) {
    return <div>Loading</div>;
  }
  return (
    <>
      <Video
        id={id}
        preview={data?.data?.urls.preview}
        checksum={data?.data?.checksum}
        video={data.data.original_url}
      />
      <Text>{data.data.description}</Text>
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
        {data.data.frames &&
          data.data.frames.map((item) => (
            <GridItem key={item.id}>
              <Arguments
                description={item.description}
                time={item.time}
                id={item.id}
                url={item.url}
              />
            </GridItem>
          ))}
      </Grid>
    </>
  );
};
export default SingleVideo;
