import { Button } from "@consta/uikit/Button";
import { Card } from "@consta/uikit/Card";
import { Grid, GridItem } from "@consta/uikit/Grid";
import { Text } from "@consta/uikit/Text";
import { TextField } from "@consta/uikit/__internal__/src/components/TextField";
import axios from "axios";
import { Controller, set, useForm } from "react-hook-form";
import React from "react";
const AddVideo = () => {
  const [loading, setLoading] = React.useState(false);
  const { control, handleSubmit } = useForm({
    defaultValues: {
      url: "",
      description: "",
    },
  });
  const onSubmit = (data) => {
    console.log(data);
    const add = async () => {
      setLoading(true);
      const response = await axios.post(
        `${import.meta.env.VITE_APIHOST}/upload/url`,
        data
      );
      console.log(response);
      setLoading(false);
    };
    add();
  };
  if (loading) {
    return <div>Идет добавление видео...</div>;
  }
  return (
    <Grid cols={1} xAlign="center" yAlign="center">
      <GridItem>
        <Card style={{ padding: "20px" }}>
          <Text size="2xl" align="center">
            Добавить видео
          </Text>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Controller
              name="url"
              control={control}
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

            <Controller
              name="description"
              control={control}
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

            <Button
              type="submit"
              label="Отправить"
              style={{ marginTop: "20px" }}
            ></Button>
          </form>
        </Card>
      </GridItem>
    </Grid>
  );
};

export default AddVideo;
