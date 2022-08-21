
# Movie Reviews API - fastAPI
Backend for my movie reviews. using [fastAPI](https://fastapi.tiangolo.com/)
# Links
[Website Link](https://movies.piuroprauxy.ml/) | [Website Source](https://github.com/yPiuro/moviereviews) | [API Link](https://api.piuroprauxy.ml/)

## Environment Variables

To run this project, you will need to add the following environment variables to your project

### General env

`PORT`

### token.env

`TOKEN`

## API Reference

#### Get all reviews (title,content,id,rating)

```http
  GET /reviews
```

#### Get random value as json

```http
  GET /random
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `min`      | `int` | Minium value of the range of random ints |
| `max`      | `int` | Max value of the range of random ints |

```http
  POST /reviews/add
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | token for simple serverside auth |

| Body - Key | value    | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | Movie title for review |
| `content`      | `string` | Review content |
| `rating`      | `float` | (Optional) Movie rating for review |

```http
  DELETE /reviews/remove
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | token for simple serverside auth |
| `id`      | `int` | Id of movie getting removed |


```http
  PUT /reviews/update
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | token for simple serverside auth |
| `id`      | `int` | Id of movie getting updated |

| Body - Key | value    | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | Movie title for updated review |
| `content`      | `string` | Updated review content |
| `rating`      | `float` | Updated movie rating for review (Higher than 5 will remove rating) |

# Requirements

Python 3.10

[pip requirements](https://raw.githubusercontent.com/yPiuro/moviesapi/main/requirements.txt)

## Run locally

To deploy this project locally run

```bash
  pip install -r requirements.txt && python main.py
```

## Deployemnet

Dockerfile coming soon...

```bash
  COMING SOON
```

## Authors

- [@yPiuro](https://www.github.com/octokatherine) - Main Developer.
- [@notliam99](https://github.com/Notliam99) - Hosting/Server Provider. ♥