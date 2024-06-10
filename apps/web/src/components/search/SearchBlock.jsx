import React from "react";
import { AutoComplete } from "@consta/uikit/AutoComplete";
import { FieldGroup } from "@consta/uikit/FieldGroup";
import { Button } from "@consta/uikit/Button";
import PropTypes from "prop-types";
import { Select } from "@consta/uikit/Select";
import { useLocation } from "react-router-dom";
const SearchBlock = ({ handleSearch }) => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const [value, setValue] = React.useState(searchParams.get("query") || null);

  const [priotitet, setPriotitet] = React.useState({
    video: parseInt(searchParams.get("video")) || 90,
    audio: parseInt(searchParams.get("audio")) || 80,
    text: parseInt(searchParams.get("text")) || 20,
    hashtag: parseInt(searchParams.get("hashtag")) || 30,
  });
  const items = [
    {
      label: "Чёрный",

      id: 1,
    },
    {
      label: "Белый",
      id: 2,
    },
    {
      label: "Синий",
      id: 3,
    },
    {
      label: "Красный",
      id: 4,
    },
    {
      label: "Сине-зелёный",
      id: 5,
    },
    {
      label: "Красно-коричневый",
      id: 6,
    },
  ];
  const preVideo = [
    {
      label: 10,
    },
    {
      label: 20,
    },
    {
      label: 30,
    },
    {
      label: 40,
    },
    {
      label: 50,
    },
    {
      label: 60,
    },
    {
      label: 70,
    },
    {
      label: 80,
    },
    {
      label: 90,
    },
    {
      label: 100,
    },
  ];

  return (
    <>
      <div>
        <FieldGroup size="m">
          <AutoComplete
            type="text"
            placeholder="Начните вводить запрос"
            value={value}
            items={items}
            onChange={setValue}
          />
          <Button
            label="Искать"
            onClick={() => handleSearch(value, priotitet)}
          />
        </FieldGroup>
      </div>
      <div>
        <h3 style={{ textAlign: "left" }}>Задайте приоритеты поиска</h3>
        <FieldGroup size="m">
          <Select
            label="По видео"
            items={preVideo}
            value={{ label: priotitet.video }}
            onChange={(item) =>
              setPriotitet({ ...priotitet, video: item.label })
            }
          />
          <Select
            label="По аудио"
            items={preVideo}
            value={{ label: priotitet.audio }}
            onChange={(item) =>
              setPriotitet({ ...priotitet, audio: item.label })
            }
          />
          <Select
            label="По тексту"
            items={preVideo}
            value={{ label: priotitet.text }}
            onChange={(item) =>
              setPriotitet({ ...priotitet, text: item.label })
            }
          />
          <Select
            label="По хэштегам"
            items={preVideo}
            value={{ label: priotitet.hashtag }}
            onChange={(item) =>
              setPriotitet({ ...priotitet, hashtag: item.label })
            }
          />
        </FieldGroup>
      </div>
    </>
  );
};

SearchBlock.propTypes = {
  handleSearch: PropTypes.func.isRequired,
};

export default SearchBlock;
