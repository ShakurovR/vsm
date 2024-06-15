import { Button } from "@consta/uikit/Button";
import { Card } from "@consta/uikit/Card";
import { Grid, GridItem } from "@consta/uikit/Grid";
import { Text } from "@consta/uikit/Text";
import { TextField } from "@consta/uikit/__internal__/src/components/TextField";
import axios from "axios";
import { Controller, useForm } from "react-hook-form";
import React from "react";
import Video from "../components/video/Video";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";

const schema = yup
  .object({
    url: yup.string().url().required(),
    description: yup.string().required(),
  })
  .required();

const AddVideo = () => {
  const [loading, setLoading] = React.useState(false);
  const [video, setVideo] = React.useState(null);
  const [error, setError] = React.useState();
  const {
    control,
    handleSubmit,
    resetField,
    formState: { errors },
  } = useForm({
    defaultValues: {
      url: "",
      description: "",
    },
    resolver: yupResolver(schema),
  });
  const onSubmit = async (data) => {
    console.log(data);
    try {
      setLoading(true);
      const response = await axios.post(
        `${import.meta.env.VITE_APIHOST}/upload/url`,
        data
      );
      setVideo(response);
      console.log(response);
      setLoading(false);
    } catch (e) {
      console.error(e);
      setError(e?.response?.data?.detail || "Что-то пошло не так");
    } finally {
      setLoading(false);
    }
  };
  if (loading) {
    return <div>Идет добавление видео...</div>;
  }
  if (error) {
    return (
      <>
        <Grid cols={1} xAlign="center" yAlign="center">
          <GridItem>
            <Card style={{ padding: "20px" }}>
              <Text size="2xl" align="center">
                {error}
              </Text>
            </Card>
          </GridItem>
        </Grid>
        <Button
          label="Попробовать еще раз"
          style={{ marginTop: "20px" }}
          onClick={() => {
            setError(null);
          }}
        />
      </>
    );
  }
  if (video) {
    return (
      <>
        <Grid cols={1} xAlign="center" yAlign="center">
          <GridItem>
            <Text>Видео добавлено и скоро будет проидексировано!</Text>
            <Card style={{ padding: "20px" }}>
              <Video
                id={video?.data?.id}
                preview={video?.data?.urls?.preview}
                checksum={video?.data?.checksum}
                video={video?.data?.original_url}
                single={true}
                desc={video?.data?.description}
              />
            </Card>
          </GridItem>
        </Grid>
        <Button
          label="Добавить еще одно"
          size="m"
          view="primary"
          style={{
            backgroundColor: "#000",
            width: "200px",
            margin: "20px auto",
          }}
          onClick={() => {
            setVideo(null);
            resetField("url");
            resetField("description");
          }}
        />
      </>
    );
  }
  return (
    <Grid cols={1} xAlign="center" yAlign="center">
      <GridItem>
        <Card style={{ padding: "20px", width: "100%", minWidth: "320px" }}>
          <Text size="2xl" align="center">
            Добавить видео
          </Text>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Controller
              name="url"
              control={control}
              required
              render={({ field }) => (
                <TextField
                  placeholder="Прямая ссылка на видео"
                  {...field}
                  required
                  name="url"
                  style={{ paddingTop: "20px" }}
                />
              )}
            />
            <Text> {errors.url?.message} </Text>
            <Controller
              name="description"
              control={control}
              required
              render={({ field }) => (
                <TextField
                  placeholder="Описание видео"
                  {...field}
                  required
                  name="description"
                  style={{ paddingTop: "20px" }}
                />
              )}
            />
            <Text>{errors.description?.message}</Text>
            <Button
              type="submit"
              label="Отправить"
              view="primary"
              style={{ marginTop: "20px", backgroundColor: "#000" }}
            ></Button>
          </form>
        </Card>
      </GridItem>
    </Grid>
  );
};

export default AddVideo;
