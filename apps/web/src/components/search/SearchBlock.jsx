import React from "react";
import { AutoComplete } from "@consta/uikit/AutoComplete";
import { FieldGroup } from "@consta/uikit/FieldGroup";
import { Button } from "@consta/uikit/Button";
import PropTypes from "prop-types";
import { Select } from "@consta/uikit/Select";
import { useLocation } from "react-router-dom";
import { sugg } from "../../data/sugg";
import { preVideo } from "../../data/preVideo";
import Fuse from "fuse.js";
const SearchBlock = ({ handleSearch }) => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const [value, setValue] = React.useState(searchParams.get("query") || null);
  const [suggestions, setSuggestions] = React.useState(sugg);

  const [priotitet, setPriotitet] = React.useState({
    video: parseInt(searchParams.get("video")) || 90,
    audio: parseInt(searchParams.get("audio")) || 80,
    text: parseInt(searchParams.get("text")) || 20,
    hashtag: parseInt(searchParams.get("hashtag")) || 30,
  });
  const fuseOptions = {
    keys: ["label"], // Ключи объекта, по которым будет выполняться поиск
    threshold: 0.35, // Порог схожести для размытого поиска
  };
  const fuse = new Fuse(sugg, fuseOptions);
  const handleInputChange = (inputValue) => {
    const results = fuse.search(inputValue); // Выполняем поиск по введенному значению
    const searchSuggestions = results.map((result) => result.item);
    // Обновляем список подсказок в AutoComplete
    setSuggestions(searchSuggestions);
    console.log(suggestions);
    return results.map((result) => result.item);
  };
  React.useEffect(() => {
    value && handleInputChange(value);
  }, [value]);

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSearch(value, priotitet);
    }
  };

  return (
    <>
      <div>
        <FieldGroup size="m">
          <AutoComplete
            type="text"
            placeholder="Начните вводить запрос"
            value={value}
            items={suggestions}
            onChange={setValue}
            onKeyDown={handleKeyDown}
            searchFunction={(suggestions, searchValue) => {
              if (!searchValue) {
                return true;
              }
              return suggestions.label.toLocaleLowerCase();
            }}
          />
          <Button
            label="Искать"
            onClick={() => handleSearch(value, priotitet)}
            className="btn_black"
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
            label="По тегам"
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
